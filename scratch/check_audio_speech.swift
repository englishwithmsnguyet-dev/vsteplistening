import Foundation
import Speech

let url = URL(fileURLWithPath: "scratch/sample_550.wav")
guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")), recognizer.isAvailable else {
    print("Recognizer not available")
    exit(1)
}

let request = SFSpeechURLRecognitionRequest(url: url)
recognizer.recognitionTask(with: request) { result, error in
    if let result = result {
        if result.isFinal {
            print("Transcript: \(result.bestTranscription.formattedString)")
            exit(0)
        }
    } else if let error = error {
        print("Error: \(error)")
        exit(1)
    }
}
RunLoop.main.run(until: Date().addingTimeInterval(5))
