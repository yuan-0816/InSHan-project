import customtkinter
from CTkMessagebox import CTkMessagebox
from tkinter.filedialog import askopenfile
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class main_window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.FileName = ""
        self.IsOpenFile = False

        FontStyle = customtkinter.CTkFont(size=20, family="Arial")

        self.title("影像辨識與車流偵測")
        self.geometry(f"{1440}x{720}")
        self.iconbitmap('icon.ico')
        # self.resizable(False, False)

        self.grid_columnconfigure((0), weight=2)
        self.grid_rowconfigure((1), weight=2)

        # Show Result Frame
        self.ResultFrame = customtkinter.CTkFrame(self)
        self.ResultFrame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        # Direction
        self.label_Direction = customtkinter.CTkLabel(self.ResultFrame, text="方向", font=FontStyle)
        self.label_Direction.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label_Direction_E = customtkinter.CTkLabel(self.ResultFrame, text="East", font=FontStyle)
        self.label_Direction_E.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.label_Direction_S = customtkinter.CTkLabel(self.ResultFrame, text="South", font=FontStyle)
        self.label_Direction_S.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.label_Direction_W = customtkinter.CTkLabel(self.ResultFrame, text="West", font=FontStyle)
        self.label_Direction_W.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.label_Direction_N = customtkinter.CTkLabel(self.ResultFrame, text="North", font=FontStyle)
        self.label_Direction_N.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Quantity
        self.label_Quantity = customtkinter.CTkLabel(self.ResultFrame, text="數量", font=FontStyle)
        self.label_Quantity.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label_Quantity_E = customtkinter.CTkLabel(self.ResultFrame, text="0", font=FontStyle)
        self.label_Quantity_E.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.label_Quantity_S = customtkinter.CTkLabel(self.ResultFrame, text="1", font=FontStyle)
        self.label_Quantity_S.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.label_Quantity_W = customtkinter.CTkLabel(self.ResultFrame, text="2", font=FontStyle)
        self.label_Quantity_W.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.label_Quantity_N = customtkinter.CTkLabel(self.ResultFrame, text="3", font=FontStyle)
        self.label_Quantity_N.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        # Average Speed
        self.label_AverageSpeed = customtkinter.CTkLabel(self.ResultFrame, text="平均速度(km/h)", font=FontStyle)
        self.label_AverageSpeed.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.label_AverageSpeed_E = customtkinter.CTkLabel(self.ResultFrame, text="0", font=FontStyle)
        self.label_AverageSpeed_E.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.label_AverageSpeed_S = customtkinter.CTkLabel(self.ResultFrame, text="0", font=FontStyle)
        self.label_AverageSpeed_S.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.label_AverageSpeed_W = customtkinter.CTkLabel(self.ResultFrame, text="0", font=FontStyle)
        self.label_AverageSpeed_W.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.label_AverageSpeed_N = customtkinter.CTkLabel(self.ResultFrame, text="0", font=FontStyle)
        self.label_AverageSpeed_N.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

        # Congestion
        self.label_Congestion = customtkinter.CTkLabel(self.ResultFrame, text="擁擠度", font=FontStyle)
        self.label_Congestion.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.label_Congestion_E = customtkinter.CTkLabel(self.ResultFrame, text="低", font=FontStyle)
        self.label_Congestion_E.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        self.label_Congestion_S = customtkinter.CTkLabel(self.ResultFrame, text="高", font=FontStyle)
        self.label_Congestion_S.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.label_Congestion_W = customtkinter.CTkLabel(self.ResultFrame, text="低", font=FontStyle)
        self.label_Congestion_W.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

        self.label_Congestion_N = customtkinter.CTkLabel(self.ResultFrame, text="低", font=FontStyle)
        self.label_Congestion_N.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

        # Play Video Frame
        self.PlayVideoFrame = customtkinter.CTkFrame(self)
        self.PlayVideoFrame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nswe")

        self.label_Video = customtkinter.CTkLabel(self.PlayVideoFrame, text="請選擇影片", font=customtkinter.CTkFont(size=20, family="Arial"))
        self.label_Video.place(relx=0.5, rely=0.5, anchor="center")

        # Result Graph Frame
        self.ResultGraphFrame = customtkinter.CTkFrame(self)
        self.ResultGraphFrame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nswe")

        self.label_GraphTitle = customtkinter.CTkLabel(self.ResultGraphFrame, text="各方向車流量", font=customtkinter.CTkFont(size=20, family="Arial", weight="bold"))
        self.label_GraphTitle.place(relx=0.5, rely=0.06, anchor='center')
        self.canvas = customtkinter.CTkCanvas(self.ResultGraphFrame, width=350, height=340)
        self.canvas.place(relx=0.5, rely=0.55, anchor="center")

        # Button Frame
        self.ButtonFrame = customtkinter.CTkFrame(self)
        self.ButtonFrame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.OpenFileBtn = customtkinter.CTkButton(self.ButtonFrame, text='選擇影片',
                                                   font=customtkinter.CTkFont(size=20, family="Arial"),
                                                   command=lambda:self.open_file())
        self.OpenFileBtn.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.OpenLiveBtn = customtkinter.CTkButton(self.ButtonFrame, text='選擇直播',
                                               font=customtkinter.CTkFont(size=20, family="Arial"))
        self.OpenLiveBtn.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.StartBtn = customtkinter.CTkButton(self.ButtonFrame, text='開始檢測',
                                               font=customtkinter.CTkFont(size=20, family="Arial"),
                                               command=lambda:self.start())
        self.StartBtn.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        self.OpenPathBtn = customtkinter.CTkButton(self.ButtonFrame, text='開啟資料夾',
                                                    font=customtkinter.CTkFont(size=20, family="Arial"),
                                                    command=lambda:self.OpenFilePath())
        self.OpenPathBtn.grid(row=0, column=3, padx=10, pady=10, sticky="n")

        # self.DrawResult()

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
        if file is not None:
            self.FileName = file.name
            print(self.FileName)
            self.IsOpenFile = True

    def start(self):
        if self.IsOpenFile:
            self.CapVideo(True)
        else:
           CTkMessagebox(title="Error", message="未選擇檔案！", icon="cancel")

    def CapVideo(self, IsOpenVideo):
        if IsOpenVideo is True:
            self.cap = cv2.VideoCapture(self.FileName)
            self.label_Video.configure(text="")
            self.update()

    def update(self):
        # Disabled Button
        self.OpenFileBtn.configure(state='disabled')
        self.OpenLiveBtn.configure(state='disabled')
        self.StartBtn.configure(state='disabled')
        self.OpenPathBtn.configure(state='disabled')

        ret, frame = self.cap.read()
        if ret == True:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image).resize((1080, 600))
            imgtks = ImageTk.PhotoImage(image=img)

            self.label_Video.imgtk = imgtks
            self.label_Video.configure(image=imgtks)
            self.label_Video.after(2, self.update)
        else:
            self.label_Video.configure(image="", text="請選擇影片", font=customtkinter.CTkFont(size=20, family="Arial"))
            self.DrawResult()
            self.IsOpenFile = False
            self.OpenFileBtn.configure(state='normal')
            self.OpenLiveBtn.configure(state='normal')
            self.StartBtn.configure(state='normal')
            self.OpenPathBtn.configure(state='normal')

    def DrawResult(self):
        data = [8, 6, 12, 2]
        dir = ["E", "S", "W", "N"]
        fig = plt.figure(figsize=(4.5, 4.5))
        plt.subplot()
        plt.pie(data,
            radius=1,
            labels=dir,
            textprops={'weight':'bold', 'size':10},
            autopct='%.1f%%',
            wedgeprops={'linewidth':3, 'edgecolor':'w'})
        # plt.show()
        self.canvas1 = FigureCanvasTkAgg(fig, self.canvas)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def UpdateLabel(self, label, num):
        # This is change label text method
        # self.label_Direction.configure(text=str)
        pass

    def OpenFilePath(self):
        self.path = os.path.dirname(self.FileName)
        os.startfile(self.path)

if __name__ == "__main__":
    app = main_window()
    app.mainloop()
