import AVFoundation
import Foundation

class AudioRecorder: NSObject, AVAudioRecorderDelegate {
    var audioRecorder: AVAudioRecorder?
    let fileName = "test_recording17.m4a"
    
    override init() {
        super.init()
        requestMicrophoneAccess()
    }
    
    func requestMicrophoneAccess() {
        #if os(iOS) || os(tvOS)
        // iOS and iPadOS: Use AVAudioSession to request microphone access
        switch AVAudioSession.sharedInstance().recordPermission {
        case .granted:
            print("Microphone access already granted.")
            startRecording()
            
        case .denied:
            print("Microphone access denied.")
            
        case .undetermined:
            AVAudioSession.sharedInstance().requestRecordPermission { granted in
                DispatchQueue.main.async {
                    if granted {
                        print("Microphone access granted.")
                        self.startRecording()
                    } else {
                        print("Microphone access denied.")
                    }
                }
            }
            
        @unknown default:
            print("Unknown microphone authorization status.")
        }
        
        #elseif os(macOS)
        // macOS: Use AVCaptureDevice to request microphone access
        switch AVCaptureDevice.authorizationStatus(for: .audio) {
        case .authorized:
            print("Microphone access already granted.")
            startRecording()
            
        case .denied:
            print("Microphone access denied.")
            
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .audio) { granted in
                DispatchQueue.main.async {
                    if granted {
                        print("Microphone access granted.")
                        self.startRecording()
                    } else {
                        print("Microphone access denied.")
                    }
                }
            }
            
        case .restricted:
            print("Microphone access is restricted.")
            
        @unknown default:
            print("Unknown microphone authorization status.")
        }
        #endif
    }
    
    func startRecording() {
        let audioFilename = getDownloadsDirectory().appendingPathComponent(fileName)
        print("Audio file will be saved to:", audioFilename.path)
        
        // Audio settings for high-quality m4a file
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 44100,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        do {
            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder?.delegate = self
            audioRecorder?.record(forDuration: 10)  // Record for 10 seconds
            print("Recording started. Please speak now...")
        } catch {
            print("Failed to start recording:", error)
        }
    }
    
    func stopRecording() {
        audioRecorder?.stop()
        print("Recording stopped. Audio file should be saved in Downloads folder.")
    }
    
    func getDownloadsDirectory() -> URL {
        #if os(macOS)
        return FileManager.default.urls(for: .downloadsDirectory, in: .userDomainMask).first!
        #else
        // For iOS and iPadOS, save in Documents directory
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        #endif
    }
}

// Start the recording
let recorder = AudioRecorder()
RunLoop.main.run(until: Date(timeIntervalSinceNow: 11)) // Keep the app running for the duration of recording
