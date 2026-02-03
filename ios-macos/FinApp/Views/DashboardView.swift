import SwiftUI

struct DashboardView: View {
    @StateObject private var viewModel = DashboardViewModel()
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header
                VStack(alignment: .leading) {
                    Text("Dashboard")
                        .font(.largeTitle)
                        .bold()
                    Text("Welcome to your financial overview")
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                
                // Stats Grid
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 16) {
                    StatCard(
                        title: "Total Balance",
                        value: formatCurrency(viewModel.stats?.totalBalance ?? 0),
                        change: "+5.2%",
                        isPositive: true
                    )
                    
                    StatCard(
                        title: "Monthly Income",
                        value: formatCurrency(viewModel.stats?.monthlyIncome ?? 0),
                        change: "+2.1%",
                        isPositive: true
                    )
                    
                    StatCard(
                        title: "Monthly Expenses",
                        value: formatCurrency(viewModel.stats?.monthlyExpenses ?? 0),
                        change: "-3.5%",
                        isPositive: true
                    )
                    
                    StatCard(
                        title: "Investment Value",
                        value: formatCurrency(viewModel.stats?.investmentValue ?? 0),
                        change: "+8.7%",
                        isPositive: true
                    )
                }
                .padding(.horizontal)
                
                // Recent Transactions
                VStack(alignment: .leading, spacing: 12) {
                    Text("Recent Transactions")
                        .font(.title2)
                        .bold()
                        .padding(.horizontal)
                    
                    if viewModel.recentTransactions.isEmpty {
                        EmptyStateView(
                            icon: "creditcard",
                            title: "No recent transactions",
                            message: "Your recent transactions will appear here"
                        )
                    } else {
                        ForEach(viewModel.recentTransactions.prefix(5)) { transaction in
                            TransactionRow(transaction: transaction)
                        }
                    }
                }
                .padding()
                .background(Color(.systemBackground))
                .cornerRadius(12)
                .shadow(radius: 2)
                .padding(.horizontal)
            }
            .padding(.vertical)
        }
        .task {
            await viewModel.loadData()
        }
        .onReceive(NotificationCenter.default.publisher(for: .dataDidChange)) { _ in
            Task {
                await viewModel.loadData()
            }
        }
    }
    
    private func formatCurrency(_ value: Decimal) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        return formatter.string(from: value as NSDecimalNumber) ?? "$0.00"
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let change: String
    let isPositive: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
                .textCase(.uppercase)
            
            Text(value)
                .font(.title)
                .bold()
            
            HStack(spacing: 4) {
                Image(systemName: isPositive ? "arrow.up" : "arrow.down")
                Text(change)
            }
            .font(.caption)
            .foregroundColor(isPositive ? .green : .red)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

struct EmptyStateView: View {
    let icon: String
    let title: String
    let message: String
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 48))
                .foregroundColor(.secondary)
            
            Text(title)
                .font(.headline)
            
            Text(message)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(40)
        .frame(maxWidth: .infinity)
    }
}

@MainActor
class DashboardViewModel: ObservableObject {
    @Published var stats: DashboardStats?
    @Published var recentTransactions: [Transaction] = []
    @Published var isLoading = false
    
    private let apiService = APIService()
    
    func loadData() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            // TODO: Replace with actual user ID from auth
            let userId = 1
            
            async let statsTask = apiService.fetchDashboardStats(userId: userId)
            async let transactionsTask = apiService.fetchTransactions(userId: userId)
            
            stats = try await statsTask
            recentTransactions = try await transactionsTask
        } catch {
            print("Error loading dashboard: \(error)")
        }
    }
}
