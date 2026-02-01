import SwiftUI

@main
struct FinAppApp: App {
    @StateObject private var syncService = SyncService()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(syncService)
        }
        #if os(macOS)
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
        #endif
    }
}
