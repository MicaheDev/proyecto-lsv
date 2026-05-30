import { useEffect, useRef } from "react";
import {
  FilesetResolver,
  HandLandmarker,
  type HandLandmarkerResult,
} from "@mediapipe/tasks-vision";

// Keep this outside the component so it doesn't re-initialize on every render
const vision = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm",
);
const handLandmarker = await HandLandmarker.createFromOptions(vision, {
  baseOptions: {
    modelAssetPath: "/hand_landmarker.task",
  },
  numHands: 2,
});

type Props = {};

export default function VisionLandMark({}: Props) {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  function processResults(detections: HandLandmarkerResult) {
    // Only log if we actually see hands, to keep the console readable
    if (detections.landmarks.length > 0) {
      console.log(detections.landmarks);
    }
  }

  useEffect(() => {
    let animationFrameId: number;
    let lastVideoTime = -1;
    let localStream: MediaStream | null = null;

    async function setupTracking() {
      // 1. Set the running mode to VIDEO
      await handLandmarker.setOptions({ runningMode: "VIDEO" });

      // 2. Request the webcam stream
      // Reemplaza la parte del try/catch del getUserMedia por una lógica de selección:
      try {
        // Si deseas listar los dispositivos disponibles para encontrar el de VDO.Ninja:
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(
          (device) => device.kind === "videoinput",
        );

        // Buscamos si existe la cámara virtual de VDO.Ninja o alguna ipcam activa
        const vdoNinjaDevice = videoDevices.find(
          (d) => d.label.includes("VDO.Ninja") || d.label.includes("Virtual"),
        );

        localStream = await navigator.mediaDevices.getUserMedia({
          video: {
            deviceId: vdoNinjaDevice
              ? { exact: vdoNinjaDevice.deviceId }
              : undefined,
            width: 640,
            height: 480,
          },
        });

        if (videoRef.current) {
          videoRef.current.srcObject = localStream;
          await videoRef.current.play();
        }
      } catch (err) {
        console.error("Error accessing webcam: ", err);
        return;
      }

      // 3. Start the render loop
      function renderLoop(): void {
        const video = videoRef.current;

        // CRITICAL CHECK: Ensure the video is active and actually has valid dimensions
        if (
          video &&
          video.readyState >= video.HAVE_ENOUGH_DATA &&
          video.currentTime !== lastVideoTime
        ) {
          try {
            const detections = handLandmarker.detectForVideo(
              video,
              performance.now(), // performance.now() provides a highly accurate timestamp
            );
            processResults(detections);
            lastVideoTime = video.currentTime;
          } catch (error) {
            console.error("MediaPipe processing error:", error);
          }
        }

        animationFrameId = requestAnimationFrame(renderLoop);
      }

      renderLoop();
    }

    setupTracking();

    // 4. Cleanup when the component unmounts
    return () => {
      cancelAnimationFrame(animationFrameId);
      if (localStream) {
        localStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div style={{ position: "relative" }}>
      <video
        width={300}
        height={600}
        ref={videoRef}
        style={{ transform: "scaleX(-1)" }} // Mirrors the video for a natural user experience
        playsInline
        muted
      />
    </div>
  );
}
