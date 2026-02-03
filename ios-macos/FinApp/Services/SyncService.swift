import Foundation
import Combine

/// Service for real-time synchronization across web, iOS, and macOS apps
class SyncService: ObservableObject {
    @Published var isConnected = false
    @Published var lastSyncDate: Date?
    @Published var syncError: String?
    
    private var webSocketTask: URLSessionWebSocketTask?
    private let apiService = APIService()
    private var syncTimer: Timer?
    
    init() {
        startPollingSync()
    }
    
    // MARK: - WebSocket Connection (for real-time sync)
    func connectWebSocket(userId: Int) {
        let url = URL(string: "ws://localhost:8000/ws/sync/\(userId)")!
        webSocketTask = URLSession.shared.webSocketTask(with: url)
        webSocketTask?.resume()
        isConnected = true
        
        receiveMessage()
    }
    
    private func receiveMessage() {
        webSocketTask?.receive { [weak self] result in
            switch result {
            case .success(let message):
                self?.handleWebSocketMessage(message)
                self?.receiveMessage() // Continue listening
            case .failure(let error):
                print("WebSocket error: \(error)")
                self?.isConnected = false
            }
        }
    }
    
    private func handleWebSocketMessage(_ message: URLSessionWebSocketTask.Message) {
        switch message {
        case .string(let text):
            print("Received sync message: \(text)")
            // Trigger data refresh
            NotificationCenter.default.post(name: .dataDidChange, object: nil)
        case .data(let data):
            print("Received binary data: \(data)")
        @unknown default:
            break
        }
    }
    
    func disconnectWebSocket() {
        webSocketTask?.cancel(with: .goingAway, reason: nil)
        isConnected = false
    }
    
    // MARK: - Polling Sync (fallback when WebSocket not available)
    private func startPollingSync() {
        // Poll every 30 seconds for changes
        syncTimer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { [weak self] _ in
            self?.performSync()
        }
    }
    
    private func performSync() {
        Task {
            do {
                // Check server health and trigger sync
                let isHealthy = try await apiService.checkHealth()
                if isHealthy {
                    lastSyncDate = Date()
                    NotificationCenter.default.post(name: .dataDidChange, object: nil)
                }
            } catch {
                syncError = error.localizedDescription
            }
        }
    }
    
    // MARK: - Manual Sync
    func triggerManualSync() {
        performSync()
    }
    
    deinit {
        syncTimer?.invalidate()
        disconnectWebSocket()
    }
}

// MARK: - Notification Names
extension Notification.Name {
    static let dataDidChange = Notification.Name("dataDidChange")
}
