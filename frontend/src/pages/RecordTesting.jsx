import { ReactMediaRecorder } from "react-media-recorder";

const RecordTesting = () => (
  <div className="flex flex-col items-center gap-4 p-8">
    <ReactMediaRecorder
      video
      render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
        <div className="flex flex-col items-center gap-4">
          <p className="text-lg font-medium capitalize">{status}</p>
          <div className="flex gap-4">
            <button
              onClick={startRecording}
              className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700"
            >
              Start Recording
            </button>
            <button
              onClick={stopRecording}
              className="rounded bg-red-600 px-4 py-2 text-white hover:bg-red-700"
            >
              Stop Recording
            </button>
          </div>
          {mediaBlobUrl && (
            <video
              src={mediaBlobUrl}
              controls
              autoPlay
              loop
              className="mt-4 w-full max-w-2xl rounded"
            />
          )}
        </div>
      )}
    />
  </div>
);

export default RecordTesting;