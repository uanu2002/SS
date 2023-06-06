from apps import WatermarkSystem2
from preprocess import *
def main():
    watermark_system = WatermarkSystem2()
    watermark_system.mainloop()

if __name__ == '__main__':
    resize()
    main()