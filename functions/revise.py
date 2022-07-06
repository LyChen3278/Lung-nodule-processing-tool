import cv2
import numpy as np

isMouseLBDown = False
isMouseRBDown = False
circleColor = (0, 0, 0)
circleRadius = 5
lastPoint = (0, 0)
radiusPreview = np.ones((100, 100, 3), np.uint8)
radiusPreview[:] = 255

def revise(reviseFilePath, saveFilePath, maskFilePath, maskEdgeFilePath,jsonPath):
    '''
    jsonPath: 新添加json文件路径，用于将修改的图片保存在json文件中，用于后续的体积等指标计算。
    '''
    ## img=cv2.resize(cv2.imread(reviseFilePath),(1024,1024))
    img = cv2.imread(reviseFilePath)

    def draw_circle(event,x,y,flags,param): 
        global isMouseLBDown,isMouseRBDown
        # global color
        global lastPoint

        if event == cv2.EVENT_LBUTTONDOWN:
            isMouseLBDown = True
            cv2.circle(img,(x,y), int(circleRadius/2), (0,0,0),-1)
            lastPoint = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            isMouseLBDown = False
        elif event == cv2.EVENT_MOUSEMOVE:
            if isMouseLBDown:
                cv2.line(img, pt1=lastPoint, pt2=(x, y), color=(0,0,0), thickness=circleRadius)
                lastPoint = (x, y)
                
        
        if event == cv2.EVENT_RBUTTONDOWN:
            isMouseRBDown = True
            cv2.circle(img,(x,y), int(circleRadius/2), (255,255,255),-1)
            lastPoint = (x, y)
        elif event == cv2.EVENT_RBUTTONUP:
            isMouseRBDown = False
        elif event == cv2.EVENT_MOUSEMOVE:
            if isMouseRBDown:
                cv2.line(img, pt1=lastPoint, pt2=(x, y), color=(255,255,255), thickness=circleRadius)
                lastPoint = (x, y)

    def updateCircleRadius(x):
        global circleRadius
        global radiusPreview

        circleRadius = cv2.getTrackbarPos('Circle_Radius', 'image')
        # 重置画布
        radiusPreview[:] = (255, 255, 255)
        # 绘制圆形
        cv2.circle(radiusPreview, center=(50, 50), radius=int(circleRadius / 2), color=(0, 0, 0), thickness=-1)

    cv2.namedWindow('image')
    cv2.namedWindow('radiusPreview')

    cv2.createTrackbar('Circle_Radius','image',1,20,updateCircleRadius)
    cv2.setMouseCallback('image',draw_circle)

    while(True):
        cv2.imshow('radiusPreview', radiusPreview)
        cv2.imshow('image',img)  
        if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:  
            break
        if cv2.waitKey(1) == ord('s'):
            ## 保存医生修改过的图片
            cv2.imwrite(saveFilePath,img)
            img_raw = cv2.imread(reviseFilePath)
            # img_revised = cv2.imread(saveFilePath)
            img_revised = img

            ## 根据修改过的图片和原图生成掩膜图片
            maskz = img_raw - img_revised
            maskz[maskz!=0] = 255
            cv2.imwrite(maskFilePath,maskz)

            ## 对掩膜图片使用Canny算子得到中空的只有边缘的掩膜
            img_mask = cv2.imread(maskFilePath)
            img_maskEdge = cv2.Canny(img_mask,1,50)
            cv2.imwrite(maskEdgeFilePath,img_maskEdge)

            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    revise(r"F:\肺结节\demo\project\wangcuifang\wangcuifang1\processImage\mhdpng\wangcuifang1_01.png","demo.png")

