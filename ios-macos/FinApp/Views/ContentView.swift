import SwiftUI

struct ContentView: View {
    @EnvironmentObject var syncService: SyncService
    @State private var selectedTab = 0
    
    var body: some View {
        #if os(iOS)
        iOSContent
        #else
        macOSContent
        #endif
    }
    
    // MARK: - iOS Layout
    private var iOSContent: some View {
        TabView(selection: $selectedTab) {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "chart.bar.fill")
                }
                .tag(0)
            
            AccountsView()
                .tabItem {
                    Label("Accounts", systemImage: "building.columns.fill")
                }
                .tag(1)
            
            TransactionsView()
                .tabItem {
                    Label("Transactions", systemImage: "creditcard.fill")
                }
                .tag(2)
            
            InvestmentsView()
                .tabItem {
                    Label("Investments", systemImage: "chart.line.uptrend.xyaxis")
                }
                .tag(3)
        }
        .overlay(alignment: .top) {
            if syncService.isConnected {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                    Text("Synced")
                        .font(.caption)
                }
                .padding(8)
                .background(.ultraThinMaterial)
                .cornerRadius(8)
                .padding(.top, 8)
            }
        }
    }
    
    // MARK: - macOS Layout
    private var macOSContent: some View {
        NavigationSplitView {
            List(selection: $selectedTab) {
                NavigationLink(value: 0) {
                    Label("Dashboard", systemImage: "chart.bar.fill")
                }
                
                NavigationLink(value: 1) {
                    Label("Accounts", systemImage: "building.columns.fill")
                }
                
                NavigationLink(value: 2) {
                    Label("Transactions", systemImage: "creditcard.fill")
                }
                
                NavigationLink(value: 3) {
                    Label("Investments", systemImage: "chart.line.uptrend.xyaxis")
                }
                
                NavigationLink(value: 4) {
                    Label("Payroll", systemImage: "briefcase.fill")
                }
                
                NavigationLink(value: 5) {
                    Label("Retirement", systemImage: "leaf.fill")
                }
                
                NavigationLink(value: 6) {
                    Label("Taxes", systemImage: "doc.text.fill")
                }
            }
            .navigationTitle("FinApp")
            .toolbar {
                ToolbarItem {
                    Button {
                        syncService.triggerManualSync()
                    } label: {
                        Image(systemName: "arrow.triangle.2.circlepath")
                    }
                }
            }
        } detail: {
            Group {
                switch selectedTab {
                case 0: DashboardView()
                case 1: AccountsView()
                case 2: TransactionsView()
                case 3: InvestmentsView()
                default: DashboardView()
                }
            }
        }
    }
}
