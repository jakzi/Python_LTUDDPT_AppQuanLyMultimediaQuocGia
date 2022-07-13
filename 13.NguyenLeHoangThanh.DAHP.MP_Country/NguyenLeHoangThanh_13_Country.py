# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 19:20:22 2021

@author: thanh
"""
import cv2 #xử lí computer vision 
import os #thao tác với tài nguyên máy tính 
import datetime #lấy thời gian 
import speech_recognition as sr#Nhận dạng tiếng nói
from PIL import Image, ImageTk #Thư viện hình ảnh Python 
import tkinter as tk#thư viện giao diện 
from tkinter import filedialog as fd
from tkinter import ttk
from googletrans import Translator # google dịch 
import googletrans
import playsound #Thư viện phát âm thanh 
from gtts import gTTS #Thư viện Chuyển văn bản thành giọng nói 
import numpy as np #Thư viện tính toán ma trận 
from ffpyplayer.player import MediaPlayer #Mở audio của video 
"""Hằng va biến """
#Đường dẫn 
res_mic="13NLHT_Res/mic01.png"#ảnh microphone 
res_mf="13NLHT_Res/folder.png"#ảnh folder 
res_bg="13NLHT_Res/bg.jpg"#ảnh nền 
res_ico="13NLHT_Res/world-globe.ico"#ảnh icon 
data_adress="13NLHT_Img"#Vị trí lưu file ảnh để xử lí 

#kích thước cửa sổ 
height=640
widht=480
#ngôn ngữ 
language_list=googletrans.LANGUAGES# lấy danh sách mã ngôn ngữ của thư viện 
d1=list(language_list.values())#lấy danh sách tên ngôn ngữ 
d2=list(language_list)#lấy  danh sách mã ngôn ngữ 
#màu sắc  
color_1="#01bbfe"
color_2="#000039"
#Dữ liệu quốc gia 
Data=[["vi","Việt Nam","Vietnam"],
      ["en","Anh Quốc","England"],
      ["jp","Nhật Bản","Japan"]]
main_lang=0#Chọn ngôn ngữ mặc định 
title=["13 - Nguyễn Lê Hoàng Thanh - Nhận diện quốc gia","13 - Nguyen Le Hoang Thanh - Country Detect"]
tBtn_info=["Thông tin quốc gia","Country information"]
tBtn_trans=["Nhận diện ngôn ngữ","Translate"]
tBtn_detect=["Nhận diện quốc gia","Country Detected"]
images=[]#Dữ liệu ảnh quốc kỳ, quốc huy 
#nhập dữ liệu vào images 
for  i in Data:
    quocky=cv2.imread("13NLHT_Res/QuocGia/{}/QK.jpg".format(i[0]))
    quochuy=cv2.imread("13NLHT_Res/QuocGia/{}/QH.png".format(i[0]))
    images.append(quocky)
    images.append(quochuy)
"""Hàm """
#Nhận diện ảnh với hàm sift của opencv 
sift = cv2.SIFT_create()
#Trích xuất đặc trưng của dữ liệu mẫu 
def findDes(images):
    desList=[]
    for img in images:
        img=resize(img)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        kp, des = sift.detectAndCompute(img, None)#trích xuất đặc trưng 
        desList.append(des)#lưu đặc trưng 
    return desList
#Trích xuất đặc trưng của ảnh cần xử lí và so sánh, tìm ảnh mẫu giống nhất 
def findID(img, desList,thres=15 ):
    img=resize(img)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp2, des2 = sift.detectAndCompute(img, None)#trích xuất đặc trưng 
    bf = cv2.BFMatcher() 

    matchList=[]
    finalVal =-1
    try:
        #kiểm tra kết quả phù hợp bằng cách kiểm tra của Lowe  
        for des in desList:
            matches = bf.knnMatch(des,des2,k=2)#tìm 2 bộ giống nhất của điểm đặc trưng thuộc des trong des2 
            good=[]
            for m,n in matches:
                if m.distance <0.75 *n.distance:#0.75 là tỉ lệ theo lowe ,distance là khoảng cách giữa các điểm
                    good.append([m])#nếu khoảng cách m,n quá gần thì chúng không đủ khác biệt nên loại bỏ và ngược lại  
            matchList.append(len(good))#số điểm đặc trưng phù hợp điều kiện 
    except:
        pass
    #print(max(matchList))
    # kiểm tra số điểm phù hợp có đủ nhiều để xác định không 
    if len(matchList)!=0:
        if max(matchList) > thres:
            finalVal= matchList.index(max(matchList))
    return  finalVal
#Chuyển văn bản thành giọng nói 
def speak(text,lang):
    tts = gTTS(text=text, lang=lang) #chuyển văn bản thành giọng nói
    audiofile = '13NLHT_Audio/13NguyenLeHoangThanh.mp3'
    if os.path.exists(audiofile):
        os.remove(audiofile)
    else:
        print(audiofile)
    tts.save(audiofile)#lưu file âm thanh 
    try:
        playsound.playsound(audiofile)#phát file âm thanh  
    except:
        pass
#Lưu giá trị biến 
def func(var):
  func.variable = var 
  
def fc(var):
  fc.variable = var
  
def m_lang(var):
  m_lang.variable = var  
m_lang(main_lang)#Hàm lưu biến ngôn ngữ mặc định 
# thay đổi kích thước ảnh theo tỉ lệ với chiều cao (mặc định 300 pixel )
def resize(img,size_h=300):
    (h, w, d) = img.shape# kích thước ảnh màu 
    s=size_h/h
    w=int(w*s)
    h=int(h*s)
    dim=(w,h)#kích thước mới 
    resized = cv2.resize(img, dim)#thay đổi kích thước 
    return resized
#Chọn file 
def select_file():
    filetypes = (
        ('All files', '*.*'),
        ('video files', '*.mp4;*.mov'),
        ('image files', '*.jpg;*.png')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    return filename#trả về đường dẫn 
#Nghe người dùng nói 
def talk(lang="vi",sour=sr.Microphone()):#Nhận diện giọng nói nhập dữ liệu
    query=''
    r = sr.Recognizer()
    with sour as source:
        print("Điều chỉnh tiếng ồn  ")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Nói...")
        try:
            audio_data = r.listen(source)
        except:
            audio_data = r.record(source)
        print("Kết quả...")
        try:
            query = r.recognize_google(audio_data,language=lang)
        except:
            print("Lỗi")
        print(str(query))
    return str(query)
# xoay ảnh (img: hình ảnh, g : góc quay)
def rotate(img,g):
    (h, w,d) = img.shape # kích thước ảnh 
    center = (w // 2, h // 2)#vị trị giữa 
    M = cv2.getRotationMatrix2D(center, g, 1.0) #ma trận biến đổi theo góc g 
    rotated = cv2.warpAffine(img, M, (w, h))#xoay ảnh 
    return rotated #trả về kết quả 
#cắt ảnh theo tọa độ 
def cutimg(img,h1,h2,w1,w2):
    p= img[h1:h2,w1:w2]#cắt ảnh 
    return p
# chuyển ảnh xám theo The weighted method  
def rgb_to_gray(img):
        grayImage = np.zeros(img.shape) #tạo ảnh rỗng 
        #lấy ma trận màu  
        R = np.array(img[:, :, 0])
        G = np.array(img[:, :, 1])
        B = np.array(img[:, :, 2])
        #Lấy giá trị màu xám theo The weighted method  
        R = (R *.299)
        G = (G *.587)
        B = (B *.114)
        Avg = (R+G+B)
        grayImage = img.copy()
        #chuyển thành ảnh xám 
        for i in range(3):
           grayImage[:,:,i] = Avg
        return grayImage
#Sliding window 
def apply_sliding_window(img, kernel, padding=0, stride=1): 
    h, w = img.shape[:2]
    img_p = np.zeros([h+2*padding, w+2*padding]) 
    img_p[padding:padding+h, padding:padding+w] = img 
    kernel = np.array(kernel) # lập cửa sổ trượt
    assert len(kernel.shape) == 2 and kernel.shape[0] == kernel.shape[1]
    assert kernel.shape[0] % 2 != 0
    
    k_size = kernel.shape[0] 
    k_half = int(k_size/2)
    
    y_pos = [v for idx, v in enumerate(list(range(k_half, h-k_half))) if idx % stride == 0] 
    x_pos = [v for idx, v in enumerate(list(range(k_half, w-k_half))) if idx % stride == 0] 
    
    new_img = np.zeros([len(y_pos), len(x_pos)]) 
    for new_y, y in enumerate(y_pos):
        for new_x, x in enumerate(x_pos):
            if k_half == 0: 
                pixel_val = img_p[y, x] * kernel 
            else:
                pixel_val = np.sum(img_p[y-k_half:y-k_half+k_size, x-k_half:x-k_half+k_size] * kernel)          
            new_img[new_y, new_x] = pixel_val
    return new_img
def apply_sliding_window_on_3_channels(img, kernel, padding=0, stride=1):
    layer_blue = apply_sliding_window(img[:,:,0], kernel, padding, stride) 
    layer_green = apply_sliding_window(img[:,:,1], kernel, padding, stride) 
    layer_red = apply_sliding_window(img[:,:,2], kernel, padding, stride)
    new_img = np.zeros(list(layer_blue.shape) + [3])
    new_img[:,:,0], new_img[:,:,1], new_img[:,:,2] = layer_blue, layer_green, layer_red 
    return new_img

"""Giao diện """
class App:#Cửa sổ chính 
    def __init__(self, root):
        self.main_lang=main_lang#ngôn ngữ mặc định 
        root.title(title[self.main_lang])#title 
        root.geometry('480x240')#kích thước 
        root.iconbitmap(res_ico)#icon 
        root.resizable(False, False)#chặn resize cửa sổ 
        bg=tk.Label(root,image=background)#ảnh nền 
        bg.place(x=0,y=0)
        #tên phần mềm 
        self.lbl = tk.Label(root, 
                       text=tBtn_detect[self.main_lang],font=("Arial Bold", 24),
                       fg=color_1,bg=color_2,anchor="center")
        self.lbl.place(x=90,y=20,width=300)
        #nút input file âm thanh 
        btn_aip=tk.Button(root,
                          image = mic_file,borderwidth=1,
                          activebackground=color_1,bg=color_2,
                          command=self.btn_auiput)
        btn_aip.place(x=240,y=70,width=40,height=40 )
        #nút input bằng microphone 
        btn_mic=tk.Button(root,
                          image = mic_photo,borderwidth=1,
                          activebackground=color_1,bg=color_2,
                          command=self.btn_mic_clicked )
        btn_mic.place(x=200,y=70,width=40,height=40 )
        #nút thay đổi ngôn ngữ 
        self.btn_lag=tk.Button(root,
                          image = vn_lan,borderwidth=1,
                          activebackground=color_1,bg=color_2,
                          command=self.btn_lang )
        self.btn_lag.place(x=430,y=10,width=40,height=40 )
        #nút chức năng nhận diện quốc kỳ, quốc huy 
        self.btn1 = tk.Button(root,
                         text=tBtn_detect[self.main_lang],
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,fg="#fff",
                         command=self.btn1_clicked)
        self.btn1.place(x=20,y=120,width=440,height=30)
        #nút chức năng dịch ngôn ngữ 
        self.btn2 = tk.Button(root,
                         text=tBtn_trans[self.main_lang],
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,fg="#fff",
                         command=self.btn2_clicked)
        self.btn2.place(x=20,y=160,width=440,height=30)
        #nút chức năng xem thông tin quốc gia 
        self.btn3 = tk.Button(root,
                         text=tBtn_info[self.main_lang],
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.btn3_clicked)
        self.btn3.place(x=20,y=200,width=440,height=30)
    def btn_lang(self):#thay đổi ngôn ngữ phần mềm 
        #đổi ngôn ngữ 
        if self.main_lang==0:
            self.main_lang=1
            self.btn_lag.configure(image=en_lan)
        elif self.main_lang==1:
            self.main_lang=0
            self.btn_lag.configure(image=vn_lan)
        m_lang(self.main_lang)
        #đổi ngôn ngữ hiển thị của các chức năng 
        root.title(title[self.main_lang])
        self.btn1.configure(text=tBtn_detect[self.main_lang])
        self.btn2.configure(text=tBtn_trans[self.main_lang])
        self.btn3.configure(text=tBtn_info[self.main_lang])
        self.lbl.configure(text=tBtn_detect[self.main_lang])
        pass
    def btn_auiput(self):#input file âm thanh 
        nguon=select_file()
        print(nguon)
        dulieu=talk(Data[self.main_lang][0],sr.AudioFile(nguon)).lower()
        #so sánh kết quả 
        if dulieu==tBtn_detect[self.main_lang]:
            window = NhanDienQK()
            window.grab_set()
        if dulieu==tBtn_trans[self.main_lang]:
            window = NhanDienNgonNgu()
            window.grab_set()
        if dulieu==tBtn_info[self.main_lang]:
            window = ThongTinQuocGia()
            window.grab_set()
        if dulieu=="thay đổi ngôn ngữ" or dulieu=="change language":
            self.btn_lang()
        pass
    def btn_mic_clicked(self):#input bằng microphone 
        dulieu=talk(Data[self.main_lang][0]).lower()
        #so sánh kết quả 
        if dulieu==tBtn_detect[self.main_lang].lower():
            window = NhanDienQK()
            window.grab_set()
        if dulieu==tBtn_trans[self.main_lang].lower():
            window = NhanDienNgonNgu()
            window.grab_set()
        if dulieu==tBtn_info[self.main_lang].lower():
            window = ThongTinQuocGia()
            window.grab_set()
        if dulieu=="thay đổi ngôn ngữ" or dulieu=="change language":
            self.btn_lang()
        pass
    def btn1_clicked(self):#chức năng nhận diện quốc kỳ, quốc huy 
        window = NhanDienQK()
        window.grab_set()
        pass
    def btn2_clicked(self):#chức năng dịch ngôn ngữ 
        window=NhanDienNgonNgu()
        window.grab_set()
        pass
    def btn3_clicked(self):#chức năng xem thông tin 
        window=ThongTinQuocGia()
        window.grab_set()
        pass

class NhanDienQK(tk.Toplevel):#Cửa sổ chọn nguồn cho chức năng nhận diện 
    
    def __init__(self, master = None):
        super().__init__(master = master)
        self.main_lang=m_lang.variable#ngôn ngữ
        self.title(title[self.main_lang])#title 
        self.geometry('480x240')#kích thước 
        self.iconbitmap(res_ico)#icon 
        self.resizable(False, False)#chặn resize cửa sổ 
        bg=tk.Label(self,image=background)#nền 
        bg.place(x=0,y=0)
        #tên phần mềm 
        lbl = tk.Label(self, 
                       text=tBtn_detect[self.main_lang],
                       font=("Arial Bold", 24),
                       fg=color_1,
                       bg=color_2,
                       anchor="center")
        lbl.place(x=90,y=20,width=300)
        #nút mic 
        btn_mic=tk.Button(self,
                          image = mic_photo,
                          borderwidth=1,
                          activebackground=color_1,
                          bg=color_2,
                          command=self.btn_mic
                          )
        btn_mic.pack(side = tk.TOP,pady = 70)
        #nút chọn nguồn camera 
        btn1 = tk.Button(self,
                         text="camera",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.btn1)
        btn1.place(x=20,y=120,width=440,height=30)
        #nút chọn nguồn từ file 
        btn2 = tk.Button(self,
                         text="file",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.btn2)
        btn2.place(x=20,y=160,width=440,height=30)
        #vị trí lưu 
        textbox=tk.Entry(self,
                        bg = "light yellow",)
        textbox.place(x=20,y=200,width=380,height=30)
        textbox.insert(0,data_adress)
        self.textbox=textbox
        btn3 = tk.Button(self,
                         text="Lưu",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.btn_save)
        btn3.place(x=400,y=200,width=60,height=30)
    def btn1(self):#chức năng nguồn camera 
        func(0)#truyền nguồn camera 
        window = NhanDienQuocKy()
        self.destroy()
        window.grab_set()
        pass
    def btn2(self):#chức năng nguồn file 
        nguon=select_file()
        func(nguon)#truyền nguồn từ file 
        window = NhanDienQuocKy()
        self.destroy()
        window.grab_set()
        pass
    def btn_save(self):#save 
        i=self.textbox.get()
        fc(i)#vị trí lưu 
        self.textbox.delete(0,tk.END)
        data_adress=i
        self.textbox.insert(0,data_adress)
        os.makedirs(data_adress)
        pass
    def btn_mic(self):#microphone 
        dulieu=talk(Data[self.main_lang][0])
        if dulieu=='camera':
            self.btn1()
        if dulieu=='file':
            self.btn2()
        pass
class NhanDienQuocKy(tk.Toplevel):#cửa sổ chức năng nhận diện 
    def __init__(self, master = None):
        super().__init__(master = master)
        self.main_lang=m_lang.variable#ngôn ngữ 
        self.title(title[self.main_lang])#title 
        self.geometry("{}x{}".format(height,widht))#kích thước 
        self.iconbitmap(res_ico)#icon 
        self.resizable(False, False)#chặn resize cửa sổ 
        bg=tk.Label(self,image=background)#nền 
        bg.place(x=0,y=0)
        self.lmain = tk.Label(self)#vị trí phát video,ảnh 
        self.lmain.pack()
        self.frame=None

        self.img_link=func.variable
        #Chụp ảnh 
        btn_snapshot  = tk.Button(self,
                         text="Snapshot",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.snapshot)
        btn_snapshot.place(x=10,y=310,width=90,height=30)
        #Lưu 
        btn_save  = tk.Button(self,text="Save",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.save)
        btn_save.place(x=100,y=310,width=90,height=30)
        #Mở ảnh đã lưu 
        btn_openfolder  = tk.Button(self,text="Gallery",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.ofolder)
        btn_openfolder.place(x=190,y=310,width=90,height=30)
        #tiến, lùi ảnh trong folder 
        btn_tien  = tk.Button(self,text=">",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.tien)
        btn_tien.place(x=370,y=310,width=90,height=30)
        btn_lui  = tk.Button(self,text="<",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.lui)
        btn_lui.place(x=280,y=310,width=90,height=30)
        #Bật tắt âm thanh video 
        btn_amthanh  = tk.Button(self,text="Sound",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.sound
                         )
        btn_amthanh.place(x=460,y=310,width=90,height=30)
        #Xoay ảnh 
        self.rote_data=0  
        lb_xoay = tk.Label( self, text="G")
        
        lb_xoay.place(x=10,y=350,width=20,height=30)
        self.tb_xoay=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_xoay.place(x=30,y=350,width=70,height=30)
        btn_xoay  = tk.Button(self,text="Rotate",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.rote)
        btn_xoay.place(x=100,y=350,width=90,height=30)
        #Ảnh xám 
        self.gray=True 
        btn_xam  = tk.Button(self,text="Gray",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.toGray)
        btn_xam.place(x=190,y=350,width=90,height=30)
        #sliding window 
        self.kernel=[[1]]
        self.padding=0
        self.stride=1
        self.checkSlideWin=True
        lb_k = tk.Label( self, text="k")
        lb_k.place(x=280,y=350,width=20,height=30)
        self.tb_k=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_k.place(x=300,y=350,width=70,height=30)
        lb_p = tk.Label( self, text="p")
        lb_p.place(x=370,y=350,width=20,height=30)
        self.tb_p=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_p.place(x=390,y=350,width=70,height=30)
        lb_s = tk.Label( self, text="s")
        lb_s.place(x=460,y=350,width=20,height=30)
        self.tb_s=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_s.place(x=480,y=350,width=70,height=30)
        btn_sw  = tk.Button(self,text="Sliding",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.sWin)
        btn_sw.place(x=550,y=350,width=90,height=30)
        #blur
        self.checkBlur=True 
        btn_blur  = tk.Button(self,text="Blur",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.blurimg)
        btn_blur.place(x=550,y=310,width=90,height=30)
        #cắt ảnh 
        self.h1=0
        self.h2=0
        self.w1=0
        self.w2=0
        self.checkcut=True
        lb_h1 = tk.Label( self, text="h1")
        lb_h1.place(x=10,y=390,width=20,height=30)
        self.tb_h1=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_h1.place(x=30,y=390,width=70,height=30)
        lb_h2 = tk.Label( self, text="h2")
        lb_h2.place(x=100,y=390,width=20,height=30)
        self.tb_h2=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_h2.place(x=120,y=390,width=70,height=30)
        lb_w1 = tk.Label( self, text="w1")
        lb_w1.place(x=190,y=390,width=20,height=30)
        self.tb_w1=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_w1.place(x=210,y=390,width=70,height=30)
        lb_w2 = tk.Label( self, text="w2")
        lb_w2.place(x=280,y=390,width=20,height=30)
        self.tb_w2=tk.Entry(self,
                            bg = "light yellow",)
        self.tb_w2.place(x=300,y=390,width=70,height=30)
        btn_cut  = tk.Button(self,text="Cut",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.cut)
        btn_cut.place(x=370,y=390,width=90,height=30)
        #cắt ảnh bằng chuột 
        self.cropping=False
        btn_cut  = tk.Button(self,text="M-Cut",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.cutm)
        btn_cut.place(x=460,y=390,width=90,height=30)
        ####Nhận diện ảnh 
        self.lb = tk.Entry(self,
                            bg = "light yellow",)
        self.lb.place(x=100,y=430,width=180,height=30)
        btn_cut  = tk.Button(self,text="Detect",bg=color_1,fg="#fff",
                         activebackground=color_2,
                         activeforeground=color_1,
                         command=self.detect_img)
        btn_cut.place(x=10,y=430,width=90,height=30)
        ###
        #mở 
        self.open_f()
        #đóng 
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    def resetLB(self):#reset lại các thuộc tính label phát video 
        self.lmain.destroy()
        self.lmain = tk.Label(self)
        self.lmain.pack()
    def cutm(self):#Cắt ảnh bằng chuột 
        def mouse_crop(event, x, y, flags, param):#Cắt ảnh 
            self.w1, self.h1, self.w2, self.h2#tọa độ các điểm cắt 
            if event == cv2.EVENT_LBUTTONDOWN:#Khi nhấn chuột trái thì lấy tọa độ w1,h1 
                self.w1, self.h1, self.w2, self.h2 = x, y, x, y
                self.cropping = True
            elif event == cv2.EVENT_MOUSEMOVE:#Khi di chuyển chuột lấy tọa độ w2, h2 
                if self.cropping == True:
                    self.w2, self.h2 = x, y
            elif event == cv2.EVENT_LBUTTONUP:#Thả chuột ra lưu tọa độ w2,h2 và cho phép cắt 
                self.w2, self.h2 = x, y
                self.cropping = False 
                self.checkcut=False
                print(self.h1, self.w1, self.h2, self.w2)
                
            pass
        
        img=cv2.cvtColor( self.img_out.copy(),cv2.COLOR_BGR2RGBA)
        cv2.imshow("a",img)#hiện cửa sổ ảnh 
        cv2.setMouseCallback("a", mouse_crop)# event bấm chuột 
        while True:#Vẽ khung cắt và cắt ảnh 
            i = img.copy()
            if not self.cropping:
                cv2.imshow("a", img)
            elif self.cropping:
                cv2.rectangle(i, (self.w1, self.h1), (self.w2, self.h2), (255, 0, 0), 2)#Khung ảnh cắt 
                cv2.imshow("a", i)
            if self.checkcut==False:
                self.open_f()
                break
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.checkcut=True
        pass
    def open_f(self):
        self.resetLB()
        #Mo anh hoac video
        try:
            self.open_img()
        except:
            self.open_vid()
        pass
    def save(self):#Lưu file đã xử lí 
        ts = datetime.datetime.now()
        filename="13NLHT_Save/{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        img=cv2.cvtColor( self.img_out.copy(),cv2.COLOR_BGR2RGBA)
        cv2.imwrite(os.path.join(filename),img)
        pass
    def ofolder(self):#Mở file dữ liệu lưu ở thư mục 13NLHT_Img 
        files= []
        self.classNames  = []
        self.temp=0
        myList = os.listdir(data_adress)#lấy danh sách tệp tin
        #Lấy ảnh và tên ảnh 
        for cl in myList:
            file= cv2.imread(f'{data_adress}/{cl}',0) #đọc file ở đường dẫn 
            files.append(file)#thêm vào files
            self.classNames.append(os.path.basename(cl))#thêm tên vào className 
        self.classNames.reverse()#đảo mảng 
        self.img_link=data_adress+"/"+self.classNames[0]#Ảnh lưu gần nhất 
        self.cap.release()
        cv2.destroyAllWindows()
        try:
            self.player.close_player()
        except: 
            pass 
        self.open_f()
        pass 
    def detect_img(self):#Nhận diện hình ảnh 
        desList = findDes(images) #trích đặc trưng dữ liệu 
        id= findID(self.img_out,desList)#trích đặc trưng và nhận diện ảnh 
        fn=""
        if id==-1:
            if self.main_lang==0:
                fn="Không xác định được!"
            else:
                fn="Error: Unknown!"
        else:
            #print(id)
            x=divmod(id, 2)#vì mảng = quốc kỳ+quốc huy+...
            #print(Data[x[0]][self.main_lang+1])
            if x[1]==0:
                if self.main_lang==0:
                    y="Quốc kỳ"
                else:
                    y="Ensign:"
            elif x[1]==1:
                if self.main_lang==0:
                    y="Quốc huy"
                else:
                    y="Emblem: "  
            pass
            fn=y+" "+Data[x[0]][self.main_lang+1]
        #hiển thị kết quả 
        self.lb.delete(0,tk.END)
        self.lb.insert(tk.END, fn)
    def tien(self):#lấy ảnh tiếp theo 
        if self.temp == len(self.classNames):
            return
        else:
            self.rote_data=0 
            self.gray=True
            self.checkSlideWin=True
            self.checkcut=True
            self.checkBlur=True 
            self.temp+=1
            self.img_link=data_adress+"/"+self.classNames[self.temp]
            self.open_f()
        pass
    def lui(self):#lấy ảnh phía trước 
        if self.temp == 0:
            return
        else:
            self.rote_data=0 
            self.gray=True
            self.checkSlideWin=True
            self.checkcut=True
            self.checkBlur=True 
            self.temp-=1
            self.img_link=data_adress+"/"+self.classNames[self.temp]
            self.open_f()
        pass
    def cut(self):#cắt bằng tọa độ 
        self.checkcut=False
        self.h1=int(self.tb_h1.get())
        self.h2=int(self.tb_h2.get())
        self.w1=int(self.tb_w1.get())
        self.w2=int(self.tb_w2.get())
        self.open_f()
        pass
    def rote(self):#xoay
        i=self.tb_xoay.get()
        if i=='':
            return
        self.rote_data=int(i)
        self.open_f()
        pass
    def toGray(self):#chuyển xám 
        if self.gray:
            self.gray=False
        elif not self.gray:
            self.gray=True
        self.open_f()
        pass
    def blurimg(self):#làm mờ 
        if self.checkBlur:
            self.checkBlur=False
        else:
            self.checkBlur=True
        self.open_f()
        pass
    def sWin(self):#sliding window 
        if self.checkSlideWin:
            self.checkSlideWin=False
        elif not self.checkSlideWin:
            self.kernel=[[float(self.tb_k.get())]]
            self.padding=int(self.tb_p.get())
            self.stride=int(self.tb_s.get())
            self.checkSlideWin=True
        self.open_f()
        pass
    def open_img(self):#Mở ảnh và xử lý 
        im=cv2.imread(self.img_link)
        if not self.checkSlideWin:#sliding window 
            im=apply_sliding_window_on_3_channels(im, self.kernel,self.padding,self.stride)
            im=(im * 255).round().astype(np.uint8)#chuyển im về kiểu thích hợp để xử lí tiếp 
        cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
        cv2image=resize(cv2image)#resize 
        cv2image=rotate(cv2image, self.rote_data)#xoay 
        if self.checkcut==False:#cắt 
            cv2image=cutimg(cv2image,self.h1,self.h2,self.w1,self.w2)
        if self.gray==False: #xám 
            cv2image=rgb_to_gray(cv2image )
        if not self.checkBlur:#mờ 
            cv2image=cv2.blur(cv2image,(5,5)) 
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.img_out=cv2image#Truyền ảnh kết quả sang các chức năng khác 
        #Cập nhật ảnh 
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        pass
    def open_vid(self):#Mở video và xử lý 
        self.cap = cv2.VideoCapture(self.img_link)
        try:
            self.player = MediaPlayer(self.img_link)
        except:
            pass
        def show_frame():
            ret, self.frame = self.cap.read()
            try: #Âm thanh video 
                audio_frame, val = self.player.get_frame()
                if val != 'eof' and audio_frame is not None:
                    img, t = audio_frame
            except: 
                pass 
            self.frame
            if self.img_link==0:
                self.frame = cv2.flip(self.frame, 1)#đảo hình webcam  
            if not ret:
                return
            im=self.frame
            if not self.checkSlideWin:#sliding window 
                im=apply_sliding_window_on_3_channels(im, self.kernel,self.padding,self.stride)
                im=(im * 255).round().astype(np.uint8)#chuyển im về kiểu thích hợp để xử lí tiếp 
            cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
            cv2image=resize(cv2image)#resize 
            cv2image=rotate(cv2image, self.rote_data)#xoay 
            if self.checkcut==False:#cắt 
                cv2image=cutimg(cv2image,self.h1,self.h2,self.w1,self.w2)
            if self.gray==False: #xám 
                cv2image=rgb_to_gray(cv2image )
            if not self.checkBlur:#mờ 
                cv2image=cv2.blur(cv2image,(5,5))  
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.img_out=cv2image#truyền frame kết quả ra ngoài 
            #cập nhật 
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.after_id=self.lmain.after(25, show_frame) #mở frame tiếp theo sau 25ms 
        show_frame()#chạy hàm 
        pass
    def sound(self):#bật tắt âm thanh 
        playerVolume = self.player.get_volume()#Âm lượng hiện tại 
        print('Volume = ', playerVolume)
        if playerVolume == 0.0:
            self.player.set_volume(1.0)#Bật âm thanh 
            print('unmuted')
        else:
            self.player.set_volume(0.0)#Tắt âm thanh 
            print('muted')
        pass
    def snapshot(self):#Chụp ảnh frame đang phát 
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        try:#Lưu vào 13NLHT_Img 
            cv2.imwrite(os.path.join(fc.variable,filename), self.frame.copy())
        except:
            cv2.imwrite(os.path.join(data_adress,filename), self.frame.copy())
    def on_closing(self):#Xử lí khi thoát chức năng 
        try:
            self.cap.release()
            cv2.destroyAllWindows()
            self.player.close_player()
        except:
            pass
        self.destroy()
        pass
class NhanDienNgonNgu(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self.main_lang=m_lang.variable#ngôn ngữ 
        self.title(title[self.main_lang])#title 
        self.geometry("{}x{}".format(height,widht))#kích thước 
        self.iconbitmap(res_ico)#icon 
        self.resizable(False, False)#chặn resize cửa sổ 
        bg=tk.Label(self,image=background)#ảnh nền 
        bg.place(x=0,y=0)
        #microphone 
        btn_mic=tk.Button(self,
                          image = mic_photo,
                          borderwidth=1,
                          activebackground=color_1,
                          bg=color_2,
                          command=self.ghiAm,
                          )
        btn_mic.pack(pady=20)
        #COmbobox ngôn ngữ nguồn và ngôn ngữ đích 
        Combo_src = ttk.Combobox(self, values = d1)
        Combo_src.current(101)
        Combo_src.place(x=20,y=80,width=100,height=20)
        self.Combo_src=Combo_src
        
        Combo = ttk.Combobox(self, values = d1)
        Combo.current(21)
        Combo.place(x=20,y=280,width=100,height=20)
        self.Combo=Combo
        #text box
        gInput = tk.Text(self, 
                        bg = "light yellow")
        gInput.place(x=20,y=100,width=600,height=150)
        self.gInput=gInput
        #button 
        #Đọc nguồn 
        btn_p1=tk.Button(self,
                         text="Play SRC",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.play1,
                          )
        btn_p1.place(x=140,y=250,width=60,height=50)
        #Nhận diện ngôn ngữ nguồn 
        btn_det=tk.Button(self,
                         text="Detect",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.det,
                          )
        btn_det.place(x=200,y=250,width=60,height=50)
        #Xóa dữ liệu nhập 
        btn_cle=tk.Button(self,
                         text="Clear",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.cle,
                          )
        btn_cle.place(x=260,y=250,width=60,height=50)
        #Dịch 
        btn_tras=tk.Button(self,
                         text="Trans",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.trans,
                  )
        btn_tras.place(x=320,y=250,width=60,height=50)
        #Đọc kết quả 
        btn_p2=tk.Button(self,
                         text="Play Out",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.play2,
                          )
        btn_p2.place(x=380,y=250,width=60,height=50)
        #text hiển thị kết quả 
        gOutput = tk.Text(self, 
                      bg = "light cyan")
        gOutput.place(x=20,y=300,width=600,height=150)
        self.gOutput=gOutput

    def play1(self):#Đọc nguồn 
        text=self.gInput.get(1.0,tk.END)
        lang=d2[self.Combo_src.current()]
        speak(text,lang)
    def play2(self):#Đọc kết quả 
        text=self.gOutput.get(1.0,tk.END)
        lang=d2[self.Combo.current()]
        speak(text,lang)  
    def det(self):#Nhận diện ngôn ngữ 
        text=self.gInput.get(1.0,tk.END)#lấy dữ liệu 
        translator = Translator()#khai báo 
        lang=translator.detect(text).lang# nhận diện ngôn ngữ 
        #hiển thị ngôn ngữ lên combobox 
        for i in range(len(d2)):
            if d2[i] == lang:
                #print(i)
                self.Combo_src.current(i)
    def cle(self):#Xóa dữ liệu nhập 
        self.gInput.delete(1.0,tk.END)
        self.gOutput.delete(1.0,tk.END)
    def trans(self):#Dịch 
        self.gOutput.delete(1.0,tk.END)#xóa phần kết quả cũ 
        text=self.gInput.get(1.0,tk.END)#lấy dữ liệu đầu vào 
        i=self.Combo_src.current()#ngôn ngữ của nguồn 
        o=self.Combo.current()#ngôn ngữ của kết quả 
        translator = Translator()#khai báo 
        translated = translator.translate(text,dest=d2[o],src=d2[i])#dịch 
        self.gOutput.insert(tk.END,translated.text)#hiển thị kết quả 
        pass
    def ghiAm(self):#Microphone 
        lang=d2[self.Combo_src.current()]#Lấy ngôn ngữ input đang chọn 
        dulieu=talk(lang)#gọi hàm ghi âm 
        dulieu=dulieu+" "#lấy kết quả 
        self.gInput.insert(tk.END,dulieu)#Hiển thị kết quả 
        pass 
class ThongTinQuocGia(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self.main_lang=m_lang.variable#ngôn ngữ 
        self.title(title[self.main_lang])#title 
        self.geometry("{}x{}".format(height,widht))#kích thước 
        self.iconbitmap(res_ico)#icon 
        self.resizable(False, False)#chặn resize cửa sổ 
        bg=tk.Label(self,image=background)#nền 
        bg.place(x=0,y=0)
        #Label phát video 
        self.lm = tk.Label(self)
        self.lm.pack(side = tk.LEFT)
        self.frame=None
        #Lấy danh sách quốc gia theo ngôn ngữ chương trình 
        self.qg_ten=[]
        for  i in Data:
            self.qg_ten.append(i[self.main_lang+1])
        #Combobox quốc gia 
        Combo_src = ttk.Combobox(self, values = self.qg_ten)#giá trị hiển thị 
        Combo_src.current(self.qg_ten.index(Data[self.main_lang][self.main_lang+1]))#Quốc gia mặc định 
        Combo_src.place(x=20,y=50,width=100,height=20)
        self.quocgia=Data[self.qg_ten.index(self.qg_ten[Combo_src.current()])][0]#Lấy mã quốc gia 
        #print(self.quocgia)
        #Nut play video 
        btn_p=tk.Button(self,
                         text="Play",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.play )
        btn_p.place(x=120,y=50,width=30,height=20)
        #nut mute 
        btn_m=tk.Button(self,
                         text="Mute",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.mute )
        btn_m.place(x=150,y=50,width=30,height=20)
        #Quoc ca
        btn_qc=tk.Button(self,
                         text="anthem",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.quocca )
        btn_qc.place(x=180,y=50,width=60,height=20)
        #Quoc ky
        btn_qc=tk.Button(self,
                         text="ensign",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.quocky )
        btn_qc.place(x=240,y=50,width=60,height=20)
        #Quoc huy 
        btn_qc=tk.Button(self,
                         text="emblem",
                         activebackground=color_2,
                         activeforeground=color_1,
                         bg=color_1,
                         fg="#fff",
                         command=self.quochuy )
        btn_qc.place(x=300,y=50,width=60,height=20)
        self.Combo_src=Combo_src
        self.open_vid()
        #dong cua so 
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    def quocky(self):#Mở ảnh quốc kỳ 
        quocky=Data[self.qg_ten.index(self.qg_ten[self.Combo_src.current()])][0]#Lấy mã quốc gia đang chọn 
        v="13NLHT_Res/QuocGia/{}/QK.jpg".format(quocky)#đường dẫn file 
        self.player.toggle_pause()#Tạm dừng audio 
        #Mở ảnh 
        image = cv2.imread(v)
        image = resize(image)
        cv2.imshow("ensign",image)
        cv2.waitKey(0)
        self.player.toggle_pause()#Mở lại audio 
        pass
    def quochuy(self):#Mở ảnh quốc huy 
        quocky=Data[self.qg_ten.index(self.qg_ten[self.Combo_src.current()])][0]#Lấy mã quốc gia đang chọn 
        v="13NLHT_Res/QuocGia/{}/QH.png".format(quocky)#đường dẫn file 
        self.player.toggle_pause()#Tạm dừng audio 
        #Mở ảnh quốc huy 
        image = cv2.imread(v)
        image = resize(image)
        cv2.imshow("emblem",image)
        cv2.waitKey(0)
        self.player.toggle_pause()#Mở lại audio 
        pass
    def quocca(self):#Mở quốc ca 
        self.cap.release()
        quocca=Data[self.qg_ten.index(self.qg_ten[self.Combo_src.current()])][0]#Lấy mã quốc gia 
        v="13NLHT_Res/QuocGia/{}/QC.mp3".format(quocca)#đường dẫn file 
        self.player = MediaPlayer(v)#khai báo
        self.player.start()#chạy file âm thanh 
        pass
    def mute(self):#Bật tắt âm lượng 
        playerVolume = self.player.get_volume()#Âm lượng hiện tại 
        print('Volume = ', playerVolume)
        if playerVolume == 0.0:
            self.player.set_volume(1.0)#Bật 
            print('unmuted')
        else:
            self.player.set_volume(0.0)#Tắt 
            print('muted')
        pass
    def play(self):#Mở video giới thiệu 
        self.quocgia=Data[self.qg_ten.index(self.qg_ten[self.Combo_src.current()])][0]
        #Reset Label 
        self.lm.destroy()
        self.lm = tk.Label(self)
        self.lm.pack(side = tk.LEFT)
        #mo video 
        self.open_vid()
    def open_vid(self):#Mở video với audio 
        v="13NLHT_Res/QuocGia/{}/VID.mp4".format(self.quocgia)
        print(v)
        self.cap = cv2.VideoCapture(v)
        self.player = MediaPlayer(v)
        def show_frame():
            ret, self.frame = self.cap.read()
            #audio 
            audio_frame, val = self.player.get_frame()
            if val != 'eof' and audio_frame is not None:
                img, t = audio_frame
            #video frame   
            self.frame 
            cv2im = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            cv2image=resize(cv2im)#resize 
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lm.imgtk = imgtk
            self.lm.configure(image=imgtk) 
            self.after_id=self.lm.after(25, show_frame) #mở frame tiếp theo sau 25ms 
        show_frame()
        pass
    def on_closing(self):#tắt các chức năng khi thoát 
        try:
            self.cap.release()
            cv2.destroyAllWindows()
            self.player.close_player()
        except:
            pass
        self.destroy()
        pass
if __name__ == "__main__":
    root = tk.Tk()
    #Ảnh 
    img1=Image.open(res_mic)
    mic_photo=ImageTk.PhotoImage(img1)
    
    img2=Image.open(res_mf)
    mic_file=ImageTk.PhotoImage(img2)
    
    img3=Image.open(res_bg)
    background=ImageTk.PhotoImage(img3)
    
    img4=Image.open("D:/13.NguyenLeHoangThanh.DAHP.MP_Country/13NLHT_Res/vn.png")
    vn_lan=ImageTk.PhotoImage(img4)

    img5=Image.open("D:/13.NguyenLeHoangThanh.DAHP.MP_Country/13NLHT_Res/en.png")
    en_lan=ImageTk.PhotoImage(img5)
    #app
    app=App(root)
    root.mainloop()
