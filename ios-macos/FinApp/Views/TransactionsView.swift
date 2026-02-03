import SwiftUI

struct TransactionsView: View {
    @StateObject private var viewModel = TransactionsViewModel()
    @State private var showingAddTransaction = false
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header
                HStack {
                    VStack(alignment: .leading) {
                        Text("Transactions")
                            .font(.largeTitle)
                            .bold()
                        Text("Track your income and expenses")
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                    
                    Button {
                        showingAddTransaction = true
                    } label: {
                        Label("Add Transaction", systemImage: "plus")
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
                
                // Transactions List
                if viewModel.transactions.isEmpty {
                    EmptyStateView(
                        icon: "creditcard",
                        title: "No transactions yet",
                        message: "Add your first transaction to start tracking"
                    )
                } else {
                    LazyVStack(spacing: 1) {
                        ForEach(viewModel.transactions) { transaction in
                            TransactionRow(transaction: transaction)
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
        .task {
            await viewModel.loadTransactions()
        }
        .onReceive(NotificationCenter.default.publisher(for: .dataDidChange)) { _ in
            Task {
                await viewModel.loadTransactions()
            }
        }
        .sheet(isPresented: $showingAddTransaction) {
            AddTransactionView()
        }
    }
}

struct TransactionRow: View {
    let transaction: Transaction
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(transaction.description)
                    .font(.headline)
                
                HStack {
                    if let category = transaction.category {
                        Text(category)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    if let merchant = transaction.merchant {
                        Text("•")
                            .foregroundColor(.secondary)
                        Text(merchant)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 4) {
                Text(formatCurrency(transaction.amount))
                    .font(.headline)
                    .foregroundColor(transaction.amount >= 0 ? .green : .red)
                
                Text(formatDate(transaction.transactionDate))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(.systemBackground))
    }
    
    private func formatCurrency(_ value: Decimal) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        return formatter.string(from: value as NSDecimalNumber) ?? "$0.00"
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        return formatter.string(from: date)
    }
}

struct AddTransactionView: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            Form {
                Section("Transaction Details") {
                    Text("Add transaction form")
                }
            }
            .navigationTitle("Add Transaction")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        // TODO: Save transaction
                        dismiss()
                    }
                }
            }
        }
    }
}

@MainActor
class TransactionsViewModel: ObservableObject {
    @Published var transactions: [Transaction] = []
    @Published var isLoading = false
    
    private let apiService = APIService()
    
    func loadTransactions() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            // TODO: Replace with actual user ID from auth
            transactions = try await apiService.fetchTransactions(userId: 1)
        } catch {
            print("Error loading transactions: \(error)")
        }
    }
}

struct InvestmentsView: View {
    var body: some View {
        Text("Investments View")
            .navigationTitle("Investments")
    }
}
