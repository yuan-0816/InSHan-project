import customtkinter
from tkinter.filedialog import askopenfile
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        FontStyle = customtkinter.CTkFont(size=20, family="Arial")


        # 方向
        self.label = customtkinter.CTkLabel(self, text="方向", font=FontStyle)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="East", font=FontStyle)
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="South", font=FontStyle)
        self.label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="West", font=FontStyle)
        self.label.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="North", font=FontStyle)
        self.label.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # 數量
        self.label = customtkinter.CTkLabel(self, text="數量", font=FontStyle)
        self.label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        # 平均速度
        self.label = customtkinter.CTkLabel(self, text="平均速度(km/h)", font=FontStyle)
        self.label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="0", font=FontStyle)
        self.label.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

        # 擁擠度
        self.label = customtkinter.CTkLabel(self, text="擁擠度", font=FontStyle)
        self.label.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="低", font=FontStyle)
        self.label.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="低", font=FontStyle)
        self.label.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="低", font=FontStyle)
        self.label.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="低", font=FontStyle)
        self.label.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

class VideoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="請選擇影片", font=customtkinter.CTkFont(size=20, family="Arial"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def CapVideo(self, IsOpen):
        if IsOpen is True:
            self.cap = cv2.VideoCapture(FileName)
            self.label.configure(text="")
            self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret == True:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image).resize((1080, 600))
            imgtks = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtks
            self.label.configure(image=imgtks)
            self.label.after(2, self.update)
        else:
            self.label.configure(image="", text="請選擇影片", font=customtkinter.CTkFont(size=20, family="Arial"))



class ResultFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas = customtkinter.CTkCanvas(self, width=350, height=350)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        # self.label = customtkinter.CTkLabel(self, text="圓餅圖")
        # self.label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def DrawResult(self):
        fig = plt.figure.Figure(figsize=(5, 5), dpi=100)
        data = [8, 6, 12, 2]
        label = ["東", "南", "西", "北"]
        plt.pie(data, radius=1, label=label, textprops={'weight':'bold','size':16}, autopct='%.1f%%')


class main_window(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("影像辨識與車流偵測")
        self.geometry(f"{1440}x{720}")
        self.iconbitmap('icon.ico')

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self._frame = MyFrame(self)
        self._frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.video = VideoFrame(self)
        self.video.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nswe")

        self.openbtn = customtkinter.CTkButton(self, text='open file', font=customtkinter.CTkFont(size=20, family="Arial"), command=lambda:self.open_file())
        self.openbtn.grid(row=2, column=1, padx=10, pady=10, sticky="nswe")

        self.result = ResultFrame(self)
        self.result.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('Video Files', ["*.mp4"])])
        if file is not None:
            global FileName
            FileName = file.name
            print(FileName)
            self.video.CapVideo(True)



if __name__ == "__main__":
    app = main_window()
    app.mainloop()
