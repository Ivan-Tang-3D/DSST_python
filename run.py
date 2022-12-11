import argparse

import cv2

from tracker import KCFTracker


def tracker(cam, frame, bbox):
    tracker = KCFTracker(True, True, True)  # (hog, fixed_Window, multi_scale)
    tracker.init(bbox, frame)

    try:
        while True:
            ok, frame = cam.read()

            timer = cv2.getTickCount()
            bbox = tracker.update(frame)
            bbox = list(map(int, bbox))
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            # Put FPS
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            cv2.imshow("Tracking", frame)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
    finally:
        cv2.destroyAllWindows()
        cam.release()


def run(args):
    if args.mode == 'video':
        video = cv2.VideoCapture('无人机信标视频/IMG_6823.MOV')  # use your own compressed video
    elif args.mode == 'builtin_stream':
        video = cv2.VideoCapture(0)  # use builtin camera to collect video stream
    elif args.mode == 'outer_stream':
        video = cv2.VideoCapture(1)  # use outer camera to collect video stream
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f"fps:\t{fps}")
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(f"size:\t{size}")  # image size
    try:
        ok, frame = video.read()
        bbox = cv2.selectROI('Select ROI', frame, False)
    finally:
        cv2.destroyAllWindows()
    if min(bbox) == 0:
        exit(0)
    tracker(video, frame, bbox)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        choices=['video', 'builtin_stream', 'outer_stream'], help="Select a tracking mode.")
    args = parser.parse_args()

    run(args)
