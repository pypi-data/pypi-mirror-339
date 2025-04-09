# Std modules
import os
import struct
import zlib
import time
from collections import deque
import json
from copy import copy
from threading import Lock

# Package modules
from lepton.exceptions import (ImageShapeException,
                               BufferLengthException,
                               TimeoutException,)
from lepton.misc.cmaps import Cmaps
from lepton.misc.utilities import safe_run, ESC
from lepton.core.detector import Detector

# External modules
import cv2
import numpy as np
from scipy.signal import find_peaks


class Capture():
    def __init__(self, port, target_fps, overlay):
        self.PORT = port
        self.IMAGE_SHP = (160, 120)
        try:
            self.TARGET_DT = 1.0 / target_fps
        except:
            self.TARGET_DT = None
        
        self.FLAG_OVERLAY = overlay
        if self.FLAG_OVERLAY:
            parent = os.path.dirname(os.path.realpath(__file__))
            overlay_dirpath = os.path.join(parent, r'_media')
            with open(os.path.join(overlay_dirpath,'overlay.cdat'), 'rb') as f:
                bindat = f.read()
            decoded = zlib.decompress(bindat).split(b'DELIM')
            shape = np.frombuffer(decoded[0], dtype=np.uint8)
            decoded.pop()
            decoded.pop(0)
            self.OVERLAY_FRMS = [np.frombuffer(d,dtype=np.uint8).reshape(shape) 
                                 for d in decoded]
            self.OVERLAY_LEN = len(self.OVERLAY_FRMS)
            self.overlay_n = 0
            
        self.prev_frame_time = self._time()
        
    def __del__(self):
        self.cap.release()
    
    def __enter__(self):
        self.cap = cv2.VideoCapture(self.PORT + cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.IMAGE_SHP[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.IMAGE_SHP[1]+2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"Y16 "))
        self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
    
    def _time(self):
        return cv2.getTickCount()/cv2.getTickFrequency()
        
    def _wait_4_frametime(self):
        try: 
            while True:
                if (self._time()-self.prev_frame_time)>=self.TARGET_DT: return
        except:
            return
    
    def _overlay(self, img):
        overlay_img = -1*np.ones((160,122))
        foreground = self.OVERLAY_FRMS[self.overlay_n]
        overlay_img[:,34:-35] = foreground
        overlay_img = np.flip(overlay_img.T,axis=1)
        theta = 0.05
        tx = 33.
        ty = 0.
        sx = 0.
        sy = -0.22
        p1 = -0.0001
        p2 = -0.003
        sf = -0.28
        Hs = np.array([[1.+sf, 0.,    0.],
                       [0.,    1.+sf, 0.],
                       [0.,    0.,    1.]])
        He = np.array([[np.cos(theta), -np.sin(theta), tx],
                       [np.sin(theta),  np.cos(theta), ty],
                       [0.,             0.,            1.]])
        Ha = np.array([[1., sy, 0.],
                       [sx, 1., 0.],
                       [0., 0., 1.]])
        Hp = np.array([[1., 0., 0.],
                       [0., 1., 0.],
                       [p1, p2, 1.]])
        H = Hs@He@Ha@Hp
        overlay_img = cv2.warpPerspective(overlay_img, H, overlay_img.T.shape,
                                      borderMode=cv2.BORDER_CONSTANT,
                                      borderValue=-1)
        overlay_mask = overlay_img < 0
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        overlay_mask = cv2.dilate(overlay_mask.astype(np.uint8), 
                                  kernel, iterations=4)
        overlay_mask = np.logical_not(overlay_mask)
        overlay_mask = overlay_mask.astype(bool)
        overlay_img = (overlay_img.astype(float)/255.) * 145.0 + 20.0
        overlay_img = np.round(100*(overlay_img+273.15)).astype(np.uint16)
        img[overlay_mask] = overlay_img[overlay_mask]
        self.overlay_n = (self.overlay_n + 1) % self.OVERLAY_LEN
        return img
    
    def _decode_data(self, raw_data):
        temp_C = raw_data[:-2] * 0.01 - 273.15
        
        row_A = raw_data[-2,:80]
        row_B = raw_data[-2,80:]
        row_C = raw_data[-1,:80]
        adat=struct.unpack("<bbIIQ8x6Bh6xI4xHxxH4xHHxxHxx6H64xI12x", row_A)
        bdat=struct.unpack("<38x8H106x", row_B)
        cdat=struct.unpack("<10x5H8xHH12x4H44x?x9H44x", row_C)
        
        status = ['', ]*5
        if adat[3] & 8 == 0: status[0] = "not desired"
        elif adat[3] & 8 == 8: status[0] = "desired"
        
        if adat[3] & 48 == 0: status[1] = "never commanded"
        elif adat[3] & 48 == 16: status[1] = "imminent"
        elif adat[3] & 48 == 32: status[1] = "in progress"
        elif adat[3] & 48 == 48: status[1] = "complete"
        
        if adat[3] & 4096 == 0: status[2] = "disabled"
        elif adat[3] & 4096 == 4096: status[2] = "enabled"
        
        if adat[3] & 32768 == 0: status[3] = "not locked out"
        elif adat[3] & 32768 == 32768: status[3] = "locked out"
        
        if adat[3] & 1048576 == 0: status[4] = "not imminent"
        elif adat[3] & 1048576 == 1048576: status[4] = "within 10s"

        video_format = ''
        if adat[24] == 3: video_format = 'RGB888'
        elif adat[24] == 7: video_format = 'RAW14'
        
        gain_mode = ''
        if cdat[0] == 0: gain_mode = 'high'
        elif cdat[0] == 1: gain_mode = 'low'
        elif cdat[0] == 2: gain_mode = 'auto'
        
        eff_gain_mode = ''
        if cdat[1] == 0: eff_gain_mode = 'high'
        elif cdat[1] == 1: eff_gain_mode = 'low'
        if cdat[0] != 2: eff_gain_mode = 'not in auto mode'
        
        desired_gain_mode = ''
        if cdat[2] == 0: desired_gain_mode = gain_mode
        elif cdat[2] == 1 and cdat[0] == 0: desired_gain_mode = 'low'
        elif cdat[2] == 1 and cdat[0] == 1: desired_gain_mode = 'high'
        
        telemetry = {
            'Telemetry version':'{}.{}'.format(adat[0], adat[1]),
            'Uptime (ms)':adat[2],
            'FFC desired':status[0],
            'FFC state':status[1],
            'AGC state':status[2],
            'Shutter lockout':status[3],
            'Overtemp shutdown':status[4],
            'Serial number':adat[4],
            'g++ version':'{}.{}.{}'.format(adat[5],adat[6],adat[7]),
            'dsp version':'{}.{}.{}'.format(adat[9],adat[10],adat[11]),
            'Frame count since reboot':adat[12],
            'FPA temperature (C)':round(adat[13]*0.01 - 273.15, 2),
            'Housing temperature (C)':round(adat[14]*0.01 - 273.15, 2),
            'FPA temperature at last FFC (C)':round(adat[15]*0.01-273.15, 2),
            'Uptime at last FFC (ms)':adat[16],
            'Housing temperature at last FFC':round(adat[17]*0.01-273.15,2),
            'AGC ROI (top left bottom right)':adat[18:22],
            'AGC clip high':adat[22],
            'AGC clip low':adat[23],
            'Video format':video_format,
            'Frame min temperature (C)':float(round(np.min(temp_C),2)),
            'Frame mean temperature (C)':float(round(np.mean(temp_C), 2)),
            'Frame max temperature (C)':float(round(np.max(temp_C), 2)),
            'Assumed emissivity':round(bdat[0]/8192,2),
            'Assumed background temperature (C)':round(0.01*bdat[1]-273.15,2),
            'Assumed atmospheric transmission':round(bdat[2]/8192,2),
            'Assumed atmospheric temperature (C)':round(0.01*bdat[3]-273.15,2),
            'Assumed window transmission':round(bdat[4]/8192,2),
            'Assumed window reflection':round(bdat[5]/8192,2),
            'Assumed window temperature (C)':round(0.01*bdat[6]-273.15,2),
            'Assumed reflected temperature (C)':round(0.01*bdat[7]-273.15,2),
            'Gain mode':gain_mode,
            'Effective gain mode':eff_gain_mode,
            'Desired gain mode':desired_gain_mode,
            'Temperature switch high gain to low gain (C)':cdat[3],
            'Temperature switch low gain to high gain (C)':cdat[4],
            'Population switch high gain to low gain (%)':cdat[5],
            'Population switch low gain to high gain (%)':cdat[6],
            'Gain mode ROI (top left bottom right)':cdat[7:11],
            'TLinear enabled':str(cdat[11]),
            'TLinear resolution':round(-0.09*cdat[12]+0.1,2),
            'Spotmeter max temperature (C)':round(0.01*cdat[13]-273.15,2),
            'Spotmeter mean temperature (C)':round(0.01*cdat[14]-273.15,2),
            'Spotmeter min temperature (C)':round(0.01*cdat[15]-273.15,2),
            'Spotmeter population (px)':cdat[16],
            'Spotmeter ROI (top left bottom right)':cdat[17:],}
        return temp_C, telemetry
    
    def read(self):
        self._wait_4_frametime()
        res, im = self.cap.read()
        self.prev_frame_time = self._time()
        
        if im.shape[0]!=self.IMAGE_SHP[1]+2 or im.shape[1]!=self.IMAGE_SHP[0]:
            shp = (im.shape[0]-2,im.shape[1])
            msg = ("Captured image shape {} does not equal "
                   "expected image shape {}. Are you sure the selected "
                   "port is correct? NOTE: If captured image shape is "
                   "(61, 80) the Lepton may be seated incorrectly and you "
                   "should reseat its socket.")
            msg = msg.format(shp, self.IMAGE_SHP)
            raise ImageShapeException(msg, payload=(shp, self.IMAGE_SHP))
        
        if self.FLAG_OVERLAY:
            im = self._overlay(im)
        
        if res:
            return self._decode_data(im)
        else:
            return self._decode_data(np.zeros((self.IMAGE_SHP[1]+2,
                                               self.IMAGE_SHP[0]),
                                              dtype=np.uint16))


class Lepton():
    def __init__(self, camera_port, cmap, scale_factor, overlay):
        self.PORT = camera_port
        self.CMAP = Cmaps[cmap]
        self.SHOW_SCALE = scale_factor
        self.OVERLAY = overlay
        self.BUFFER_SIZE = 5
        self.WINDOW_NAME = 'Lepton 3.5 on Purethermal 3'
        self.LOCK = Lock()
        
        self.detector = Detector()
        
        self.temperature_C_buffer = deque()
        self.telemetry_buffer = deque()
        self.image_buffer = deque()
        self.mask_buffer = deque()
        self.frame_number = 0
        self.frame_num_prev_send = -1
        
        self.flag_streaming = False
        self.flag_recording = False
        self.flag_emergency_stop = False
        self.flag_focus_box = False
        self.flag_modding_AR = True
        self.flag_modding_fast = False
        
        self.focus_box_AR = 1.33333333
        self.focus_box_size = 0.50
        self.focus_box = [(), (), (), ()]
        self.subject_quad = [(np.nan,np.nan), (np.nan,np.nan), 
                             (np.nan,np.nan), (np.nan,np.nan)]
        self.subject_next_vert = (np.nan,np.nan)
        self.homography = None
        self.inv_homography = None

    def _mouse_callback(self, event, x, y, flags, param):
        if not self.flag_focus_box: return
        
        if event == cv2.EVENT_MBUTTONDOWN and self.homography is None:
            self.flag_modding_fast = not self.flag_modding_fast
        
        if event == cv2.EVENT_MOUSEWHEEL and self.homography is None:
            if self.flag_modding_fast:
                rate = 0.1
            else:
                rate = 0.01
            if flags > 0:
                if self.flag_modding_AR:
                    self.focus_box_AR += rate
                else:
                    self.focus_box_size += rate
            else:
                if self.flag_modding_AR:
                    self.focus_box_AR -= rate
                else:
                    self.focus_box_size -= rate
            self.focus_box_size = np.clip(self.focus_box_size, 0.01, 1.0)
            self.focus_box_AR = np.clip(self.focus_box_AR, 0.01, 
                                        min(4./(3.*self.focus_box_size), 9.99))

        if event == cv2.EVENT_RBUTTONDOWN and self.homography is None:
            self.flag_modding_AR = not self.flag_modding_AR
                
        if event == cv2.EVENT_LBUTTONDOWN:
            if (np.nan, np.nan) in self.subject_quad:
                insert_at = self.subject_quad.index((np.nan, np.nan))
                self.subject_quad[insert_at] = (x,y)
            
        if event == cv2.EVENT_MOUSEMOVE:
            self.subject_next_vert = np.array([x,y])
    
    def _warped_element(self, buffer, return_buffer=False):
        is_warped = self.flag_focus_box and not self.homography is None
        if not is_warped and return_buffer: return list(buffer)
        if not is_warped and not return_buffer: return copy(buffer[-1])
        
        buffer_len = len(buffer)
        warped_buffer = []
        for i in range(buffer_len):
            if i > 2: break
            element = copy(buffer[buffer_len-1-i])
            
            if element is None:
                if not return_buffer: return None
                warped_buffer.append(None)
                continue
            
            element = element.astype(float)
            shp = (element.shape[1]*self.SHOW_SCALE,
                   element.shape[0]*self.SHOW_SCALE)
            element = cv2.resize(element, shp)
            element = cv2.warpPerspective(element, self.homography, shp)
            (l,t), (r,b) = self.focus_box[0], self.focus_box[2]
            if not return_buffer: return element[t:b+1,l:r+1]
            warped_buffer.append(element[t:b+1,l:r+1])
            
        warped_buffer.reverse()
        return warped_buffer
    
    def _detect_front(self, detect_fronts, multiframe):
        if not detect_fronts or len(self.temperature_C_buffer)<1:
            self.mask_buffer.append(None)
            return
        
        if multiframe:
            temps = self._warped_element(self.temperature_C_buffer,
                                         return_buffer=True)
        else:
            temps = [self._warped_element(self.temperature_C_buffer,
                                         return_buffer=False)]
        mask = self.detector.front(temps, 'kmeans')
        
        if self.flag_focus_box and not self.inv_homography is None:
            shp = (120*self.SHOW_SCALE,160*self.SHOW_SCALE)
            fmask = np.zeros(shp)
            (l,t), (r,b) = self.focus_box[0], self.focus_box[2]
            fmask[t:b+1,l:r+1] = mask.astype(float)
            fmask = cv2.warpPerspective(fmask, self.inv_homography, shp[::-1])
            mask = cv2.resize(fmask, (160,120)) >= 0.25
        self.mask_buffer.append(mask)
    
    def _normalize_temperature(self, temperature_C, alpha=0.0, beta=1.0,
                               equalize=True):
        mn = np.min(temperature_C)
        mx = np.max(temperature_C)
        rn = mx - mn
        if rn==0.0: return np.zeros(temperature_C.shape)
        norm = (temperature_C-mn) * ((beta-alpha)/(mx-mn)) + alpha
        if not equalize: return norm
        
        quantized = np.round(norm*255).astype(np.uint8)
        hist = cv2.calcHist([quantized.flatten()],[0],None,[256],[0,256])
        P = (hist / 19200.0).flatten()
        median_hist =  cv2.medianBlur(P, 3).flatten()
        F = median_hist[median_hist>0]
        local_maxizers = find_peaks(F)[0]
        global_maximizer = np.argmax(F)
        F_prime = F[local_maxizers[local_maxizers>=global_maximizer]]
        if len(F_prime) == 0:
            return norm
        else:
            T = np.median(F[local_maxizers[local_maxizers>=global_maximizer]])
        P[P>T] = T
        FT = np.cumsum(P)
        DT = np.floor(255*FT/FT[-1]).astype(np.uint8)
        eq = DT[quantized] / 255.0
        return  eq

    def _temperature_2_image(self, equalize):
        image = self._normalize_temperature(self.temperature_C_buffer[-1],
                                            equalize=equalize)
        image = 255.0 * self.CMAP(image)[:,:,:-1]
        image = np.round(image).astype(np.uint8)
        self.image_buffer.append(image)
    
    def _draw_subject_quad(self, image):
        lines = []
        for i in range(4):
            j = (i+1) % 4
            lines.append([self.subject_quad[i], self.subject_quad[j]])
        lines = np.array(lines)
        
        next_vert_at = np.all(np.isnan(lines[:,1,:]),axis=1)
        if any(next_vert_at):
            next_vert_at = np.argmax(next_vert_at)
            lines[next_vert_at,1,:] = self.subject_next_vert
        
        roi_image = copy(image)
        for i, line in enumerate(lines):
            if np.any(np.isnan(line)) and i!=3: break
            if i==3 and np.any(np.isnan(line)):
                srt = np.round(lines[i-1][1]).astype(int)
            else:
                srt = np.round(line[0]).astype(int)
            end = np.round(line[1]).astype(int)
            if all(srt==end): continue
            roi_image = cv2.line(roi_image, srt, end, (255,0,255), 1) 
            
        return roi_image
    
    def _draw_focus_box(self, image, quad_incomplete):
        img_h, img_w = image.shape[0], image.shape[1] 
        box_h = int(np.round(self.focus_box_size*img_h))
        box_w = int(np.round(self.focus_box_AR*box_h))
        l = int(0.5*(img_w - box_w))
        t = int(0.5*(img_h - box_h))
        r = l + box_w - 1
        b = t + box_h - 1
        self.focus_box = [(l,t),(l,b),(r,b),(r,t)]
        
        color = [0,255,255] if quad_incomplete else [255,0,255]
        fb_image = cv2.rectangle(image, self.focus_box[0], self.focus_box[2],
                                 color, 1)
        if not quad_incomplete: return fb_image
        
        cnr=[i for i,s in enumerate(self.subject_quad) if s!=(np.nan, np.nan)]
        cnr = len(cnr)
        if cnr < 4:
            fb_image = cv2.circle(fb_image, self.focus_box[cnr], 
                                  3, [255,0,255], -1)
        
        if self.flag_modding_AR:
            txt = 'AR: {:.2f}'.format(self.focus_box_AR)
            fb_image = cv2.rectangle(fb_image,(l+2,t+2),(l+75,t+15),[0,0,0],-1)
        else:
            txt = 'Size: {:.2f}'.format(self.focus_box_size)
            fb_image = cv2.rectangle(fb_image,(l+2,t+2),(l+89,t+15),[0,0,0],-1)
        fb_image = cv2.putText(fb_image, txt, (l+4,t+14),
                               cv2.FONT_HERSHEY_PLAIN , 1, (255,255,255), 1,
                               cv2.LINE_AA)
        
        return fb_image
    
    def _focus_box(self, image):
        if not self.flag_focus_box: return image, False
        
        quad_incomplete = np.any(np.isnan(self.subject_quad))
        if quad_incomplete:
            quad_image = self._draw_subject_quad(image)
            return self._draw_focus_box(quad_image, quad_incomplete), False
        
        if self.homography is None:
            xs = np.array(self.subject_quad)
            ys = np.array(self.focus_box)
            self.homography, _ = cv2.findHomography(xs, ys)
            self.inv_homography = np.linalg.inv(self.homography)

        shp = (image.shape[1], image.shape[0])
        warped_image = cv2.warpPerspective(image, self.homography, shp)
        return self._draw_focus_box(warped_image, quad_incomplete), True
    
    def _uptime_str(self):
        telemetry = self.telemetry_buffer[-1]
        hrs = telemetry['Uptime (ms)']/3600000.0
        mns = 60.0*(hrs-np.floor(hrs))
        scs = 60.0*(mns-np.floor(mns))
        mss = 1000.0*(scs - np.floor(scs))
        hrs = int(np.floor(hrs))
        mns = int(np.floor(mns))
        scs = int(np.floor(scs))
        mss = int(np.floor(mss))
        return "{:02d}:{:02d}:{:02d}:{:03d}".format(hrs,mns,scs,mss)
    
    def _temperature_range_str(self):
        telemetry = self.telemetry_buffer[-1]
        mn = '({:0>6.2f})'.format(telemetry['Frame min temperature (C)'])
        i=1
        while mn[i]=='0' and mn[i+1]!='.':
            mn=' {}{}'.format(mn[:i], mn[i+1:])
            i+=1
        me = '| {:0>6.2f} |'.format(telemetry['Frame mean temperature (C)'])
        i=2
        while me[i]=='0' and me[i+1]!='.':
            me=' {}{}'.format(me[:i], me[i+1:])
            i+=1
        mx = '({:0>6.2f})'.format(telemetry['Frame max temperature (C)'])
        i=1
        while mx[i]=='0' and mx[i+1]!='.':
            mx=' {}{}'.format(mx[:i], mx[i+1:])
            i+=1
        return "{} {} {} C".format(mn, me, mx)
    
    def _fps_str(self):
        if len(self.telemetry_buffer)<self.BUFFER_SIZE:
            return 'FPS: ---'
        
        frame_times = []
        for i in range(self.BUFFER_SIZE):
            telemetry = self.telemetry_buffer[i-self.BUFFER_SIZE]
            frame_times.append(telemetry['Uptime (ms)'])
        if len(frame_times) <= 1:
            delta = 0.0
        else:
            delta = np.mean(np.diff(frame_times))*0.001
        if delta <= 0.0: return 'FPS: ---'
        return 'FPS: {:.2f}'.format(1.0/delta)
            
    def _telemetrize_image(self, image):
        shp = (image.shape[0]+30,image.shape[1],image.shape[2])
        telimg = np.zeros(shp).astype(np.uint8)
        telimg[:-30,:,:] = image
        
        uptime_pos = (int(np.round(telimg.shape[1]/64)), telimg.shape[0]-10)
        range_pos = (telimg.shape[1]-255, telimg.shape[0]-10)
        fps_pos = (int(np.round(0.5*(range_pos[0]+uptime_pos[0])))+20, 
                   telimg.shape[0]-10)
        
        telimg = cv2.putText(telimg, self._uptime_str(), uptime_pos, 
                             cv2.FONT_HERSHEY_PLAIN , 1, (255,255,255), 1, 
                             cv2.LINE_AA)
        telimg = cv2.putText(telimg, self._temperature_range_str(), range_pos, 
                             cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1,
                             cv2.LINE_AA)
        telimg = cv2.putText(telimg, self._fps_str(), fps_pos,
                             cv2.FONT_HERSHEY_PLAIN , 1, (255,255,255), 1,
                             cv2.LINE_AA)
        
        if self.telemetry_buffer[-1]['FFC state']=='imminent':
            telimg = cv2.rectangle(telimg,(5,5),(35,25),[0,0,0],-1)
            telimg = cv2.putText(telimg, "FFC", (6,21),
                                cv2.FONT_HERSHEY_PLAIN , 1, (255,255,255), 1,
                                cv2.LINE_AA)
        return telimg
        
    def _get_show_image(self):
        image = copy(self.image_buffer[-1])
        mask = self.mask_buffer[-1]
        if not mask is None:
            image[mask] = [0,255,0]
                
        shp = (image.shape[1]*self.SHOW_SCALE, image.shape[0]*self.SHOW_SCALE)
        image = cv2.resize(image, shp)
        
        show_im, warped = self._focus_box(image)
        rec_im = copy(show_im) if warped else image
        rec_im = self._telemetrize_image(rec_im)
        self.image_buffer[-1] = rec_im
        
        if self.flag_recording:
            show_im = cv2.circle(show_im, (show_im.shape[1]-10,10), 5,
                                 [255,0,0], -1)
        show_im = self._telemetrize_image(show_im)
        show_im = cv2.cvtColor(show_im, cv2.COLOR_BGR2RGB)
        return show_im

    def _trim_buffers(self):
        while len(self.temperature_C_buffer) > self.BUFFER_SIZE:
            self.temperature_C_buffer.popleft()
        while len(self.telemetry_buffer) > self.BUFFER_SIZE:
            self.telemetry_buffer.popleft()
        while len(self.image_buffer) > self.BUFFER_SIZE:
            self.image_buffer.popleft()
        while len(self.mask_buffer) > self.BUFFER_SIZE:
            self.mask_buffer.popleft()

    def _keypress_callback(self, wait=1):      
        key = cv2.waitKeyEx(wait)

        if key == ord('f'):
            with self.LOCK:
                self.flag_focus_box = not self.flag_focus_box
    
        if key == ord('r'):
            with self.LOCK:
                self.subject_quad = [(np.nan,np.nan), (np.nan,np.nan), 
                                     (np.nan,np.nan), (np.nan,np.nan)]
                self.subject_next_vert = (np.nan,np.nan)
                self.homography = None
                self.inv_homography = None
    
        if key == 27:
            with self.LOCK:
                self.flag_streaming = False

    def _estop_stream(self):
        msg = "Emergency stopping stream... "
        print(ESC.fail(msg), end="", flush=True)
        self.flag_emergency_stop = True
        self.flag_streaming = False
        cv2.destroyAllWindows()
        print(ESC.OKCYAN+"Stopped."+ESC.ENDC, flush=True)

    def _stream(self, fps, detect_fronts, multiframe, equalize):
        with Capture(self.PORT, fps, self.OVERLAY) as self.cap:
            if self.flag_emergency_stop:
                self._estop_stream()
                time.sleep(1.0) # Wait for other tasks out of thread
                msg = "Stream emergency stopped before starting."
                print(ESC.fail(msg), flush=True)
                return
            
            self.flag_streaming = True
            cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_AUTOSIZE) 
            cv2.setMouseCallback(self.WINDOW_NAME, self._mouse_callback)
            print(ESC.header("Stream started."), flush=True)
            print(ESC.header(''.join(['-']*60)), flush=True)
            while self.flag_streaming:
                if self.flag_emergency_stop:
                    self._estop_stream()
                    time.sleep(1.0) # Wait for other tasks out of thread
                    print(ESC.header(''.join(['-']*60)), flush=True)
                    print(ESC.header("Stream ended in emergency stop."), 
                          flush=True)
                    return
                
                temperature_C, telemetry = self.cap.read()
                with self.LOCK:
                    self.temperature_C_buffer.append(temperature_C)
                    self.telemetry_buffer.append(telemetry)
                    self._detect_front(detect_fronts, multiframe)
                    self._temperature_2_image(equalize)
                    image = self._get_show_image()
                    self._trim_buffers()
                    self.frame_number += 1
                    
                cv2.imshow(self.WINDOW_NAME, image) 
                self._keypress_callback()
                
            cv2.destroyAllWindows()
        time.sleep(1.0) # Wait for other tasks out of thread
        print(ESC.header(''.join(['-']*60)), flush=True)
        print(ESC.header("Stream ended normally."), flush=True)
    
    def _buf_len(self):
        l1 = len(self.temperature_C_buffer)
        l2 = len(self.telemetry_buffer)
        l3 = len(self.image_buffer)
        l4 = len(self.mask_buffer)
        if (l1==l2 and l2==l3 and l3==l4): return l1
        
        msg = ("An error occured while validating buffer lengths. "
               "Temperature buffer: {}, Telemetry buffer: {}, "
               "Image buffer: {}, Mask buffer: {}. "
               "This can occur when non thread safe functions are called "
               "while in thread.").format(l1, l2, l3, l4)
        payload = (self.temperature_C_buffer,
                   self.telemetry_buffer,
                   self.image_buffer,
                   self.mask_buffer,)
        raise BufferLengthException(msg, payload=payload)
    
    def _get_writable_frame(self, ignore_buf_min):
        buffer_length = self._buf_len()
        if buffer_length <= self.BUFFER_SIZE and not ignore_buf_min:
            return (None, None, None, None, )
        
        if buffer_length == 0:
            return (None, None, None, None, )

        temperature_C = self.temperature_C_buffer.popleft()
        telemetry = self.telemetry_buffer.popleft()
        image = self.image_buffer.popleft()
        mask = self.mask_buffer.popleft()
        return (temperature_C, telemetry, image, mask, )
    
    def _write_frame(self, frame_data, files):
        if all(d is None for d in frame_data): return
        temperature_C = frame_data[0]
        telemetry = frame_data[1]
        image = frame_data[2]
        mask = frame_data[3]
        
        temperature_cK = np.round(100.*(temperature_C+273.15))
        temperature_cK = temperature_cK.astype(np.uint16)
        encode_param = [int(cv2.IMWRITE_TIFF_COMPRESSION), 
                        cv2.IMWRITE_TIFF_COMPRESSION_LZW]
        T_img = cv2.imencode('.tiff', temperature_cK, encode_param)[1]
        T_img = T_img.tobytes()
        files[0].write(T_img)
        files[0].write(b'DELIM')
        
        json.dump(telemetry, files[1])
        files[1].write('DELIM')
        
        image=cv2.imencode('.png', image)[1].tobytes()
        files[2].write(image)
        files[2].write(b'DELIM')
        
        if mask is None:
            mask = np.zeros(temperature_C.shape).astype(bool)
        files[3].write(zlib.compress(mask.tobytes()))
        files[3].write(b'DELIM')
    
    def _estop_record(self):
        self._estop_stream()
        msg = "Emergency stopping record... "
        print(ESC.fail(msg), end="", flush=True)
        self.flag_emergency_stop = True
        self.flag_recording = False
        print(ESC.OKCYAN+"Stopped."+ESC.ENDC, flush=True)
    
    def _record(self, fps, detect_fronts, multiframe, equalize):
        dirname = 'rec_data'
        os.makedirs(dirname, exist_ok=True)
        fnames = ['temperature.dat', 'telem.json', 'image.dat', 'mask.dat']
        typ = ['wb', 'w', 'wb', 'wb']
        
        with (Capture(self.PORT, fps, self.OVERLAY) as self.cap,
              open(os.path.join(dirname, fnames[0]), typ[0]) as T_file,
              open(os.path.join(dirname, fnames[1]), typ[1]) as t_file,
              open(os.path.join(dirname, fnames[2]), typ[2]) as i_file,
              open(os.path.join(dirname, fnames[3]), typ[3]) as m_file,):
            if self.flag_emergency_stop:
                self._estop_record()
                time.sleep(1.0) # Wait for other tasks out of thread
                msg = "Recording emergency stopped before starting."
                print(ESC.fail(msg), flush=True)
                return
            
            self.flag_streaming = True
            self.flag_recording = True
            cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_AUTOSIZE) 
            cv2.setMouseCallback(self.WINDOW_NAME, self._mouse_callback)
            files = (T_file, t_file, i_file, m_file, )
            print(ESC.header("Recording started."), flush=True)
            print(ESC.header(''.join(['-']*60)), flush=True)
            while self.flag_streaming:
                if self.flag_emergency_stop:
                    self._estop_record()
                    time.sleep(1.0) # Wait for other tasks out of thread
                    print(ESC.header(''.join(['-']*60)), flush=True)
                    print(ESC.header("Recording ended in emergency stop."),
                          flush=True)
                    return
                
                temperature_C, telemetry = self.cap.read()
                with self.LOCK:
                    self.temperature_C_buffer.append(temperature_C)
                    self.telemetry_buffer.append(telemetry)
                    self._detect_front(detect_fronts, multiframe)
                    self._temperature_2_image(equalize)
                    image = self._get_show_image()
                    frame_data = self._get_writable_frame(ignore_buf_min=False)
                    self.frame_number += 1
                
                self._write_frame(frame_data, files)
                cv2.imshow(self.WINDOW_NAME, image) 
                self._keypress_callback()
                
            cv2.destroyAllWindows()
            
            with self.LOCK:
                term_frame_data = []
                while self._buf_len() > 0:
                    frame_data = self._get_writable_frame(ignore_buf_min=True)
                    term_frame_data.append(frame_data)
            for frame_data in term_frame_data:
                self._write_frame(frame_data, files)
            
        self.recording=False    
        time.sleep(1.0) # Wait for other tasks out of thread
        print(ESC.header(''.join(['-']*60)), flush=True)
        print(ESC.header("Recording ended normally."), flush=True)

    def emergency_stop(self):
        if not self.flag_emergency_stop:
            self.flag_emergency_stop = True
            msg="{}EMERGENCY STOP COMMAND RECEIVED{}"
            print(msg.format(ESC.FAIL, ESC.ENDC), flush=True)        

    def stop(self):
        with self.LOCK:
            self.flag_streaming = False

    def start_stream(self, fps=None, detect_fronts=False, multiframe=True, 
                     equalize=False):
        res = safe_run(self._stream, self._estop_stream,
                        args=(fps, detect_fronts, multiframe, equalize, ))   
        if res < 0:
            time.sleep(1.0) # Wait for other tasks out of thread
            print(ESC.header(''.join(['-']*60)), flush=True)
            msg = "Streaming ended in emergency stop due to exception."
            print(ESC.header(msg),flush=True)
            
        return res

    def start_record(self, fps=None, detect_fronts=False, multiframe=True, 
                     equalize=False):
        res = safe_run(self._record, self._estop_record, 
                        args=(fps, detect_fronts, multiframe, equalize))
        if res < 0:
            time.sleep(1.0) # Wait for other tasks out of thread
            print(ESC.header(''.join(['-']*60)), flush=True)
            msg = "Recording ended in emergency stop due to exception."
            print(ESC.header(msg),flush=True)
            
        return res
    
    def _wait_until(self, condition, timeout_ms, dt_ms):
        epoch_s = time.time()
        timeout_s = 0.001*timeout_ms
        dt_s = 0.001*dt_ms
        while not condition():
            if (time.time()-epoch_s) > timeout_s:
                string = "Function _wait_until({}) timed out at {} ms."
                raise TimeoutException(string.format(condition.__name__, 
                                                     timeout_ms), 
                                       timeout_s)
            time.sleep(dt_s)
            if self.flag_emergency_stop: break

    def _buffers_populated(self):
        with self.LOCK:
            return self._buf_len() > 1
    
    def wait_until_stream_active(self, timeout_ms=5000., dt_ms=25.):
        return safe_run(self._wait_until, args=(self._buffers_populated,
                                                 timeout_ms, dt_ms))   
    
    def _frame_data_to_bytes(self, frame_data):
        frame_num = frame_data[0]
        time_stamp = frame_data[1]
        temperature_cK = frame_data[2]
        mask = frame_data[3]
        
        if frame_num is None:
            f_data = b''
        else:
            f_data = np.uint64(frame_num).tobytes()
        
        if time_stamp is None:
            t_data = b''
        else:
            t_data = np.uint64(time_stamp).tobytes()
        
        if temperature_cK is None:
            T_data = b''
        else:
            T_data = np.insert(temperature_cK.flatten(),0,
                               temperature_cK.shape).tobytes()
            T_data = zlib.compress(T_data)
        
        if mask is None: 
            m_data = b''
        else:
            m_data = np.insert(mask.flatten(),0,mask.shape).tobytes()
            m_data = zlib.compress(m_data)
        
        return  (f_data, t_data, T_data, m_data, )
    
    def _get_frame_data(self, focused_ok):
        with self.LOCK:
            frame_number = copy(self.frame_number)
            if frame_number <= self.frame_num_prev_send:
                return (None, None, None, None, )
            self.frame_num_prev_send = frame_number
            
            if self._buf_len() == 0:
                return (frame_number, None, None, None, )
            
            time = round(copy(self.telemetry_buffer[-1]['Uptime (ms)'])*.001,3)
            if not focused_ok:
                temperature_C = copy(self.temperature_C_buffer[-1])
                temperature_cK = np.round(100*(temperature_C+273.15))
                temperature_cK = temperature_cK.astype(np.uint16)
                mask = copy(self.mask_buffer[-1]).astype(np.uint16)
                return (frame_number, time, temperature_cK, mask, )
            
            temperature_C = self._warped_element(self.temperature_C_buffer, 
                                                 return_buffer=False)
            mask = self._warped_element(self.mask_buffer, 
                                        return_buffer=False)
            
            if not self.flag_focus_box or self.homography is None:
                temperature_cK = np.round(100*(temperature_C+273.15))
                temperature_cK = temperature_cK.astype(np.uint16)
                if not mask is None:
                    mask = (mask >= 0.25).astype(np.uint16)
                return (frame_number, time, temperature_cK, mask, )
            
            shp=(int(np.round(temperature_C.shape[1]/self.SHOW_SCALE)),
                 int(np.round(temperature_C.shape[0]/self.SHOW_SCALE)))
            temperature_C = cv2.resize(temperature_C, shp)
            temperature_cK = np.round(100*(temperature_C+273.15))
            temperature_cK = temperature_cK.astype(np.uint16)
            if not mask is None:
                mask = cv2.resize(mask, shp)
                mask = (mask >= 0.25).astype(np.uint16)
            return (frame_number, time, temperature_cK, mask, )
    
    def get_frame_data(self, focused_ok=False, as_bytes=False):
        frame_data = self._get_frame_data(focused_ok)
        if as_bytes: return self._frame_data_to_bytes(frame_data)
        return frame_data
    
    def is_streaming(self):
        with self.LOCK:
            return copy(self.flag_streaming)
    
    def is_recording(self):
        with self.LOCK:
            return copy(self.flag_recording)
            