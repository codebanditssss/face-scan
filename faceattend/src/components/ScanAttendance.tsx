// // // import React, { useState, useEffect, useRef } from 'react';
// // // import { Camera, AlertCircle, CheckCircle } from 'lucide-react';

// // // function ScanAttendance() {
// // //   const [scanning, setScanning] = useState(false);
// // //   const [matchResult, setMatchResult] = useState(null);
// // //   const videoRef = useRef(null);
// // //   const streamRef = useRef(null);
// // //   const wsRef = useRef(null);

// // //   useEffect(() => {
// // //     return () => {
// // //       stopCamera();
// // //       if (wsRef.current) {
// // //         wsRef.current.close();
// // //       }
// // //     };
// // //   }, []);

// // //   const startCamera = async () => {
// // //     try {
// // //       const stream = await navigator.mediaDevices.getUserMedia({
// // //         video: {
// // //           width: 640,
// // //           height: 480,
// // //           facingMode: 'user'
// // //         }
// // //       });

// // //       if (videoRef.current) {
// // //         videoRef.current.srcObject = stream;
// // //         streamRef.current = stream;
// // //       }
// // //     } catch (err) {
// // //       console.error("Error accessing camera:", err);
// // //     }
// // //   };

// // //   const stopCamera = () => {
// // //     if (streamRef.current) {
// // //       streamRef.current.getTracks().forEach(track => track.stop());
// // //       if (videoRef.current) {
// // //         videoRef.current.srcObject = null;
// // //       }
// // //     }
// // //   };

// // //   const startWebSocket = () => {
// // //     wsRef.current = new WebSocket('ws://localhost:8000/ws/scan');
    
// // //     wsRef.current.onmessage = (event) => {
// // //       const data = JSON.parse(event.data);
// // //       if (data.success) {
// // //         setMatchResult({
// // //           success: true,
// // //           name: data.name,
// // //           confidence: data.confidence
// // //         });
// // //         stopScanning();
// // //       } else if (data.message === "No face detected") {
// // //         // Continue scanning
// // //         setMatchResult(null);
// // //       } else {
// // //         setMatchResult({
// // //           success: false,
// // //           message: data.message,
// // //           confidence: data.confidence || 0
// // //         });
// // //       }
// // //     };

// // //     wsRef.current.onerror = (error) => {
// // //       console.error('WebSocket error:', error);
// // //       stopScanning();
// // //     };
// // //   };

// // //   const captureAndSendFrame = () => {
// // //     if (!videoRef.current || !wsRef.current) return;

// // //     const canvas = document.createElement('canvas');
// // //     canvas.width = videoRef.current.videoWidth;
// // //     canvas.height = videoRef.current.videoHeight;
// // //     const ctx = canvas.getContext('2d');
// // //     ctx.drawImage(videoRef.current, 0, 0);

// // //     // Send frame to backend
// // //     const base64Frame = canvas.toDataURL('image/jpeg');
// // //     wsRef.current.send(base64Frame);
// // //   };

// // //   const startScanning = async () => {
// // //     setScanning(true);
// // //     setMatchResult(null);
// // //     await startCamera();
// // //     startWebSocket();

// // //     // Start sending frames
// // //     const interval = setInterval(() => {
// // //       if (wsRef.current?.readyState === WebSocket.OPEN) {
// // //         captureAndSendFrame();
// // //       }
// // //     }, 1000);

// // //     // Store interval ID for cleanup
// // //     wsRef.current.interval = interval;
// // //   };

// // //   const stopScanning = () => {
// // //     setScanning(false);
// // //     stopCamera();
// // //     if (wsRef.current) {
// // //       clearInterval(wsRef.current.interval);
// // //       wsRef.current.close();
// // //     }
// // //   };

// // //   return (
// // //     <div className="max-w-4xl mx-auto p-6">
// // //       <div className="bg-[#1e2533] rounded-lg shadow-lg p-6">
// // //         <h2 className="text-2xl font-bold text-white mb-2">Face Recognition Scanner</h2>
// // //         <p className="text-gray-400 mb-6">Position your face in front of the camera for attendance</p>

// // //         {/* Camera View */}
// // //         <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-6">
// // //           {scanning ? (
// // //             <video
// // //               ref={videoRef}
// // //               autoPlay
// // //               playsInline
// // //               className="w-full h-full object-cover"
// // //             />
// // //           ) : (
// // //             <div className="absolute inset-0 flex items-center justify-center">
// // //               <div className="text-center">
// // //                 <Camera className="h-16 w-16 text-gray-600" />
// // //                 <p className="text-gray-500 mt-2">Camera is off</p>
// // //               </div>
// // //             </div>
// // //           )}
// // //         </div>

// // //         {/* Status Indicators */}
// // //         <div className="grid grid-cols-3 gap-4 mb-6">
// // //           <div className="text-center">
// // //             <Camera className="h-6 w-6 text-blue-400 mx-auto mb-2" />
// // //             <p className="text-sm text-gray-400">Camera Status</p>
// // //             <p className="text-white">{scanning ? 'Active' : 'Inactive'}</p>
// // //           </div>

// // //           <div className="text-center">
// // //             <AlertCircle className="h-6 w-6 text-yellow-400 mx-auto mb-2" />
// // //             <p className="text-sm text-gray-400">Face Detection</p>
// // //             <p className="text-white">Ready</p>
// // //           </div>

// // //           <div className="text-center">
// // //             <CheckCircle className="h-6 w-6 text-green-400 mx-auto mb-2" />
// // //             <p className="text-sm text-gray-400">Recognition Status</p>
// // //             <p className="text-white">Waiting</p>
// // //           </div>
// // //         </div>

// // //         {/* Control Button */}
// // //         <div className="flex justify-center">
// // //           <button
// // //             onClick={scanning ? stopScanning : startScanning}
// // //             className="flex items-center px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
// // //           >
// // //             <Camera className="h-5 w-5 mr-2" />
// // //             {scanning ? 'Stop Scanning' : 'Start Scanning'}
// // //           </button>
// // //         </div>
// // //       </div>

// // //       {/* Match Result */}
// // //       {matchResult && (
// // //         <div className={`mt-6 p-4 rounded-lg ${
// // //           matchResult.success 
// // //             ? 'bg-green-500/10 border border-green-500/20' 
// // //             : 'bg-red-500/10 border border-red-500/20'
// // //         }`}>
// // //           <div className="flex items-center">
// // //             {matchResult.success ? (
// // //               <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
// // //             ) : (
// // //               <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
// // //             )}
// // //             <div>
// // //               <h3 className={`font-medium ${
// // //                 matchResult.success ? 'text-green-500' : 'text-red-500'
// // //               }`}>
// // //                 {matchResult.success ? 'Attendance Marked Successfully' : 'Recognition Failed'}
// // //               </h3>
// // //               <p className={`text-sm mt-1 ${
// // //                 matchResult.success ? 'text-green-400/80' : 'text-red-400/80'
// // //               }`}>
// // //                 {matchResult.success 
// // //                   ? `Attendance recorded for ${matchResult.name}`
// // //                   : matchResult.message || 'Please try again'
// // //                 }
// // //               </p>
// // //             </div>
// // //           </div>
// // //         </div>
// // //       )}
// // //     </div>
// // //   );
// // // }

// // // export default ScanAttendance;


// // import React, { useState, useEffect, useRef } from 'react';
// // import { Camera, AlertCircle, CheckCircle } from 'lucide-react';

// // function ScanAttendance() {
// //   const [scanning, setScanning] = useState(false);
// //   const [matchResult, setMatchResult] = useState(null);
// //   const videoRef = useRef(null);
// //   const streamRef = useRef(null);
// //   const wsRef = useRef(null);

// //   useEffect(() => {
// //     return () => {
// //       stopCamera();
// //       if (wsRef.current) {
// //         wsRef.current.close();
// //       }
// //     };
// //   }, []);

// //   const startCamera = async () => {
// //     try {
// //       const stream = await navigator.mediaDevices.getUserMedia({
// //         video: {
// //           width: 640,
// //           height: 480,
// //           facingMode: 'user'
// //         }
// //       });

// //       if (videoRef.current) {
// //         videoRef.current.srcObject = stream;
// //         streamRef.current = stream;
// //       }
// //     } catch (err) {
// //       console.error("Error accessing camera:", err);
// //     }
// //   };

// //   const stopCamera = () => {
// //     if (streamRef.current) {
// //       streamRef.current.getTracks().forEach(track => track.stop());
// //       if (videoRef.current) {
// //         videoRef.current.srcObject = null;
// //       }
// //     }
// //   };

// //   const captureAndSendFrame = () => {
// //     if (!videoRef.current || !scanning) return;

// //     const canvas = document.createElement('canvas');
// //     canvas.width = videoRef.current.videoWidth;
// //     canvas.height = videoRef.current.videoHeight;
// //     const ctx = canvas.getContext('2d');
// //     ctx.drawImage(videoRef.current, 0, 0);

// //     // Send frame to backend
// //     const base64Frame = canvas.toDataURL('image/jpeg');
// //     if (wsRef.current?.readyState === WebSocket.OPEN) {
// //       wsRef.current.send(base64Frame);
// //     }
// //   };

// //   const startScanning = async () => {
// //     setScanning(true);
// //     setMatchResult(null);
// //     await startCamera();

// //     // Setup WebSocket
// //     wsRef.current = new WebSocket('ws://localhost:8000/ws/scan');
    
// //     wsRef.current.onopen = () => {
// //       console.log('WebSocket connected');
// //       // Start sending frames after connection is established
// //       wsRef.current.frameInterval = setInterval(captureAndSendFrame, 100);
// //     };

// //     wsRef.current.onmessage = (event) => {
// //       const data = JSON.parse(event.data);
// //       if (data.success) {
// //         setMatchResult({
// //           success: true,
// //           name: data.name,
// //           confidence: data.confidence,
// //           message: "Attendance marked successfully"
// //         });
// //         stopScanning(); // Stop when successful match is found
// //       } else {
// //         setMatchResult({
// //           success: false,
// //           message: data.message
// //         });
// //       }
// //     };

// //     wsRef.current.onerror = (error) => {
// //       console.error('WebSocket error:', error);
// //       stopScanning();
// //     };

// //     wsRef.current.onclose = () => {
// //       console.log('WebSocket closed');
// //       if (wsRef.current?.frameInterval) {
// //         clearInterval(wsRef.current.frameInterval);
// //       }
// //     };
// //   };

// //   const stopScanning = () => {
// //     setScanning(false);
// //     stopCamera();
// //     if (wsRef.current) {
// //       if (wsRef.current.frameInterval) {
// //         clearInterval(wsRef.current.frameInterval);
// //       }
// //       wsRef.current.close();
// //     }
// //   };

// //   return (
// //     <div className="max-w-4xl mx-auto p-6">
// //       <div className="bg-[#1e2533] rounded-lg shadow-lg p-6">
// //         <h2 className="text-2xl font-bold text-white mb-2">Face Recognition Scanner</h2>
// //         <p className="text-gray-400 mb-6">Position your face in front of the camera for attendance</p>

// //         {/* Camera View */}
// //         <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-6">
// //           {scanning ? (
// //             <video
// //               ref={videoRef}
// //               autoPlay
// //               playsInline
// //               className="w-full h-full object-cover"
// //             />
// //           ) : (
// //             <div className="absolute inset-0 flex items-center justify-center">
// //               <div className="text-center">
// //                 <Camera className="h-16 w-16 text-gray-600" />
// //                 <p className="text-gray-500 mt-2">Camera is off</p>
// //               </div>
// //             </div>
// //           )}
// //         </div>

// //         {/* Status Indicators */}
// //         <div className="grid grid-cols-3 gap-4 mb-6">
// //           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
// //             <div className="flex items-center justify-center mb-2">
// //               <Camera className="h-6 w-6 text-blue-400" />
// //             </div>
// //             <p className="text-sm text-gray-400">Camera Status</p>
// //             <p className="text-white font-medium">{scanning ? 'Active' : 'Inactive'}</p>
// //           </div>
          
// //           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
// //             <div className="flex items-center justify-center mb-2">
// //               <AlertCircle className="h-6 w-6 text-yellow-400" />
// //             </div>
// //             <p className="text-sm text-gray-400">Face Detection</p>
// //             <p className="text-white font-medium">
// //               {scanning ? 'Processing' : 'Ready'}
// //             </p>
// //           </div>
          
// //           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
// //             <div className="flex items-center justify-center mb-2">
// //               <CheckCircle className="h-6 w-6 text-green-400" />
// //             </div>
// //             <p className="text-sm text-gray-400">Recognition Status</p>
// //             <p className="text-white font-medium">
// //               {matchResult?.success ? 'Match Found' : 'Waiting'}
// //             </p>
// //           </div>
// //         </div>

// //         {/* Control Button */}
// //         <div className="flex justify-center">
// //           <button
// //             onClick={scanning ? stopScanning : startScanning}
// //             className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center font-medium transition-colors"
// //           >
// //             <Camera className="h-5 w-5 mr-2" />
// //             {scanning ? 'Stop Scanning' : 'Start Scanning'}
// //           </button>
// //         </div>
// //       </div>

// //       {/* Match Result */}
// //       {matchResult && (
// //         <div className={`mt-6 p-4 rounded-lg ${
// //           matchResult.success 
// //             ? 'bg-green-500/10 border border-green-500/20' 
// //             : 'bg-red-500/10 border border-red-500/20'
// //         }`}>
// //           <div className="flex items-center">
// //             {matchResult.success ? (
// //               <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
// //             ) : (
// //               <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
// //             )}
// //             <div>
// //               <h3 className={`font-medium ${
// //                 matchResult.success ? 'text-green-500' : 'text-red-500'
// //               }`}>
// //                 {matchResult.success ? 'Attendance Marked Successfully' : 'Recognition Failed'}
// //               </h3>
// //               <p className={`text-sm mt-1 ${
// //                 matchResult.success ? 'text-green-400/80' : 'text-red-400/80'
// //               }`}>
// //                 {matchResult.success 
// //                   ? `Attendance recorded for ${matchResult.name}`
// //                   : matchResult.message || 'Please try again'
// //                 }
// //               </p>
// //             </div>
// //           </div>
// //         </div>
// //       )}
// //     </div>
// //   );
// // }

// // export default ScanAttendance;

// import React, { useState, useEffect, useRef } from 'react';
// import { Camera, AlertCircle, CheckCircle } from 'lucide-react';

// function ScanAttendance() {
//   const [scanning, setScanning] = useState(false);
//   const [matchResult, setMatchResult] = useState(null);
//   const [processedImage, setProcessedImage] = useState(null);
//   const videoRef = useRef(null);
//   const canvasRef = useRef(null);
//   const streamRef = useRef(null);
//   const wsRef = useRef(null);

//   useEffect(() => {
//     return () => {
//       stopCamera();
//       if (wsRef.current) {
//         wsRef.current.close();
//       }
//     };
//   }, []);

//   const startCamera = async () => {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({
//         video: {
//           width: 640,
//           height: 480,
//           facingMode: 'user'
//         }
//       });

//       if (videoRef.current) {
//         videoRef.current.srcObject = stream;
//         streamRef.current = stream;
//       }
//     } catch (err) {
//       console.error("Error accessing camera:", err);
//     }
//   };

//   const stopCamera = () => {
//     if (streamRef.current) {
//       streamRef.current.getTracks().forEach(track => track.stop());
//       if (videoRef.current) {
//         videoRef.current.srcObject = null;
//       }
//     }
//   };

//   const captureAndSendFrame = () => {
//     if (!videoRef.current || !scanning) return;

//     const canvas = document.createElement('canvas');
//     canvas.width = videoRef.current.videoWidth;
//     canvas.height = videoRef.current.videoHeight;
//     const ctx = canvas.getContext('2d');
//     ctx.drawImage(videoRef.current, 0, 0);

//     // Send frame to backend
//     const base64Frame = canvas.toDataURL('image/jpeg');
//     if (wsRef.current?.readyState === WebSocket.OPEN) {
//       wsRef.current.send(base64Frame);
//     }
//   };

//   const startScanning = async () => {
//     setScanning(true);
//     setMatchResult(null);
//     setProcessedImage(null);
//     await startCamera();

//     // Setup WebSocket
//     wsRef.current = new WebSocket('ws://localhost:8000/ws/scan');
    
//     wsRef.current.onopen = () => {
//       console.log('WebSocket connected');
//       wsRef.current.frameInterval = setInterval(captureAndSendFrame, 100);
//     };

//     wsRef.current.onmessage = (event) => {
//       const data = JSON.parse(event.data);
      
//       // Update processed image if available
//       if (data.processed_frame) {
//         setProcessedImage(data.processed_frame);
//       }

//       if (data.success) {
//         setMatchResult({
//           success: true,
//           name: data.name,
//           confidence: data.confidence,
//           message: "Attendance marked successfully"
//         });
//         // Don't stop scanning immediately on success to show the result
//         setTimeout(stopScanning, 2000);
//       } else {
//         setMatchResult({
//           success: false,
//           message: data.message || "No match found"
//         });
//       }
//     };

//     wsRef.current.onerror = (error) => {
//       console.error('WebSocket error:', error);
//       stopScanning();
//       setMatchResult({
//         success: false,
//         message: "Connection error. Please try again."
//       });
//     };

//     wsRef.current.onclose = () => {
//       console.log('WebSocket closed');
//       if (wsRef.current?.frameInterval) {
//         clearInterval(wsRef.current.frameInterval);
//       }
//     };
//   };

//   const stopScanning = () => {
//     setScanning(false);
//     stopCamera();
//     setProcessedImage(null);
//     if (wsRef.current) {
//       if (wsRef.current.frameInterval) {
//         clearInterval(wsRef.current.frameInterval);
//       }
//       wsRef.current.close();
//     }
//   };

//   return (
//     <div className="max-w-4xl mx-auto p-6">
//       <div className="bg-[#1e2533] rounded-lg shadow-lg p-6">
//         <h2 className="text-2xl font-bold text-white mb-2">Face Recognition Scanner</h2>
//         <p className="text-gray-400 mb-6">Position your face in front of the camera for attendance</p>

//         {/* Camera View */}
//         <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-6">
//           {scanning ? (
//             <>
//               {/* Original video feed (hidden) */}
//               <video
//                 ref={videoRef}
//                 autoPlay
//                 playsInline
//                 className="hidden"
//               />
//               {/* Processed frame display */}
//               {processedImage ? (
//                 <img 
//                   src={processedImage} 
//                   alt="Processed frame"
//                   className="w-full h-full object-cover"
//                 />
//               ) : (
//                 <video
//                   ref={videoRef}
//                   autoPlay
//                   playsInline
//                   className="w-full h-full object-cover"
//                 />
//               )}
//             </>
//           ) : (
//             <div className="absolute inset-0 flex items-center justify-center">
//               <div className="text-center">
//                 <Camera className="h-16 w-16 text-gray-600" />
//                 <p className="text-gray-500 mt-2">Camera is off</p>
//               </div>
//             </div>
//           )}
//         </div>

//         {/* Status Indicators */}
//         <div className="grid grid-cols-3 gap-4 mb-6">
//           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
//             <div className="flex items-center justify-center mb-2">
//               <Camera className="h-6 w-6 text-blue-400" />
//             </div>
//             <p className="text-sm text-gray-400">Camera Status</p>
//             <p className="text-white font-medium">{scanning ? 'Active' : 'Inactive'}</p>
//           </div>
          
//           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
//             <div className="flex items-center justify-center mb-2">
//               <AlertCircle className="h-6 w-6 text-yellow-400" />
//             </div>
//             <p className="text-sm text-gray-400">Face Detection</p>
//             <p className="text-white font-medium">
//               {scanning ? 'Processing' : 'Ready'}
//             </p>
//           </div>
          
//           <div className="bg-[#252d3d] rounded-lg p-4 text-center">
//             <div className="flex items-center justify-center mb-2">
//               <CheckCircle className="h-6 w-6 text-green-400" />
//             </div>
//             <p className="text-sm text-gray-400">Recognition Status</p>
//             <p className="text-white font-medium">
//               {matchResult?.success ? 'Match Found' : 'Waiting'}
//             </p>
//           </div>
//         </div>

//         {/* Control Button */}
//         <div className="flex justify-center">
//           <button
//             onClick={scanning ? stopScanning : startScanning}
//             className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center font-medium transition-colors"
//             disabled={matchResult?.success}
//           >
//             <Camera className="h-5 w-5 mr-2" />
//             {scanning ? 'Stop Scanning' : 'Start Scanning'}
//           </button>
//         </div>
//       </div>

//       {/* Match Result */}
//       {matchResult && (
//         <div className={`mt-6 p-4 rounded-lg ${
//           matchResult.success 
//             ? 'bg-green-500/10 border border-green-500/20' 
//             : 'bg-red-500/10 border border-red-500/20'
//         }`}>
//           <div className="flex items-center">
//             {matchResult.success ? (
//               <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
//             ) : (
//               <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
//             )}
//             <div>
//               <h3 className={`font-medium ${
//                 matchResult.success ? 'text-green-500' : 'text-red-500'
//               }`}>
//                 {matchResult.success ? 'Attendance Marked Successfully' : 'Recognition Failed'}
//               </h3>
//               <p className={`text-sm mt-1 ${
//                 matchResult.success ? 'text-green-400/80' : 'text-red-400/80'
//               }`}>
//                 {matchResult.success 
//                   ? `Attendance recorded for ${matchResult.name} (${matchResult.confidence.toFixed(1)}% confidence)`
//                   : matchResult.message || 'Please try again'
//                 }
//               </p>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default ScanAttendance;

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Camera, AlertCircle, CheckCircle } from 'lucide-react';

function ScanAttendance() {
  const [scanning, setScanning] = useState(false);
  const [matchResult, setMatchResult] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const wsRef = useRef(null);

  // Configurable WebSocket URL
  const WS_URL = process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:8000/ws/scan';

  useEffect(() => {
    return () => {
      stopScanning();
    };
  }, []);

  const startCamera = useCallback(async () => {
    try {
      setCameraError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      setCameraError(err.message || "Unable to access camera");
      setScanning(false);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
      streamRef.current = null;
    }
  }, []);

  const captureAndSendFrame = useCallback(() => {
    if (!videoRef.current || !scanning) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);

    // Send frame to backend
    const base64Frame = canvas.toDataURL('image/jpeg');
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(base64Frame);
    }
  }, [scanning]);

  const startScanning = useCallback(async () => {
    // Reset previous states
    setScanning(true);
    setMatchResult(null);
    setProcessedImage(null);
    setCameraError(null);

    try {
      await startCamera();

      // Setup WebSocket
      wsRef.current = new WebSocket(WS_URL);
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
        wsRef.current.frameInterval = setInterval(captureAndSendFrame, 200); // Slightly reduced frame rate
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          // Update processed image if available
          if (data.processed_frame) {
            setProcessedImage(data.processed_frame);
          }

          if (data.success) {
            setMatchResult({
              success: true,
              name: data.name,
              confidence: data.confidence,
              message: "Attendance marked successfully"
            });
            // Stop scanning after successful match
            setTimeout(stopScanning, 2000);
          } else {
            setMatchResult({
              success: false,
              message: data.message || "No match found"
            });
          }
        } catch (parseError) {
          console.error('Error parsing WebSocket message:', parseError);
          setMatchResult({
            success: false,
            message: "Error processing scan result"
          });
        }
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        stopScanning();
        setMatchResult({
          success: false,
          message: "Connection error. Please try again."
        });
      };

      wsRef.current.onclose = () => {
        console.log('WebSocket closed');
        if (wsRef.current?.frameInterval) {
          clearInterval(wsRef.current.frameInterval);
        }
      };
    } catch (error) {
      console.error('Scanning start error:', error);
      stopScanning();
    }
  }, [startCamera, captureAndSendFrame, WS_URL]);

  const stopScanning = useCallback(() => {
    setScanning(false);
    stopCamera();
    setProcessedImage(null);
    if (wsRef.current) {
      if (wsRef.current.frameInterval) {
        clearInterval(wsRef.current.frameInterval);
      }
      wsRef.current.close();
    }
  }, [stopCamera]);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-[#1e2533] rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-2">Face Recognition Scanner</h2>
        <p className="text-gray-400 mb-6">Position your face in front of the camera for attendance</p>

        {/* Camera View */}
        <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-6">
          {scanning ? (
            <>
              {/* Original video feed (hidden) */}
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="hidden"
              />
              {/* Processed frame display */}
              {processedImage ? (
                <img 
                  src={processedImage} 
                  alt="Processed frame"
                  className="w-full h-full object-cover"
                />
              ) : (
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  className="w-full h-full object-cover"
                />
              )}
            </>
          ) : (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <Camera className="h-16 w-16 text-gray-600" />
                <p className="text-gray-500 mt-2">Camera is off</p>
              </div>
            </div>
          )}
        </div>

        {/* Status Indicators */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-[#252d3d] rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <Camera className="h-6 w-6 text-blue-400" />
            </div>
            <p className="text-sm text-gray-400">Camera Status</p>
            <p className="text-white font-medium">
              {cameraError ? 'Error' : (scanning ? 'Active' : 'Inactive')}
            </p>
          </div>
          
          <div className="bg-[#252d3d] rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <AlertCircle className="h-6 w-6 text-yellow-400" />
            </div>
            <p className="text-sm text-gray-400">Face Detection</p>
            <p className="text-white font-medium">
              {scanning ? 'Processing' : 'Ready'}
            </p>
          </div>
          
          <div className="bg-[#252d3d] rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <CheckCircle className="h-6 w-6 text-green-400" />
            </div>
            <p className="text-sm text-gray-400">Recognition Status</p>
            <p className="text-white font-medium">
              {matchResult?.success ? 'Match Found' : 'Waiting'}
            </p>
          </div>
        </div>

        {/* Control Button */}
        <div className="flex justify-center">
          <button
            onClick={scanning ? stopScanning : startScanning}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center font-medium transition-colors"
            disabled={matchResult?.success}
          >
            <Camera className="h-5 w-5 mr-2" />
            {scanning ? 'Stop Scanning' : 'Start Scanning'}
          </button>
        </div>
      </div>

      {/* Camera Error */}
      {cameraError && (
        <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
            <div>
              <h3 className="font-medium text-red-500">Camera Access Error</h3>
              <p className="text-sm mt-1 text-red-400/80">{cameraError}</p>
            </div>
          </div>
        </div>
      )}

      {/* Match Result */}
      {matchResult && (
        <div className={`mt-6 p-4 rounded-lg ${
          matchResult.success 
            ? 'bg-green-500/10 border border-green-500/20' 
            : 'bg-red-500/10 border border-red-500/20'
        }`}>
          <div className="flex items-center">
            {matchResult.success ? (
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
            ) : (
              <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
            )}
            <div>
              <h3 className={`font-medium ${
                matchResult.success ? 'text-green-500' : 'text-red-500'
              }`}>
                {matchResult.success ? 'Attendance Marked Successfully' : 'Recognition Failed'}
              </h3>
              <p className={`text-sm mt-1 ${
                matchResult.success ? 'text-green-400/80' : 'text-red-400/80'
              }`}>
                {matchResult.success 
                  ? `Attendance recorded for ${matchResult.name} (${matchResult.confidence.toFixed(1)}% confidence)`
                  : matchResult.message || 'Please try again'
                }
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ScanAttendance;