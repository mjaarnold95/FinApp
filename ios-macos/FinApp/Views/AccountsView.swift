import SwiftUI

struct AccountsView: View {
    @StateObject private var viewModel = AccountsViewModel()
    @State private var showingAddAccount = false
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header
                HStack {
                    VStack(alignment: .leading) {
                        Text("Accounts")
                            .font(.largeTitle)
                            .bold()
                        Text("Manage your financial accounts")
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                    
                    Button {
                        showingAddAccount = true
                    } label: {
                        Label("Add Account", systemImage: "plus")
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
                
                // Accounts List
                if viewModel.accounts.isEmpty {
                    EmptyStateView(
                        icon: "building.columns",
                        title: "No accounts yet",
                        message: "Add your first account to get started"
                    )
                } else {
                    LazyVStack(spacing: 12) {
                        ForEach(viewModel.accounts) { account in
                            AccountCard(account: account)
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
        .task {
            await viewModel.loadAccounts()
        }
        .onReceive(NotificationCenter.default.publisher(for: .dataDidChange)) { _ in
            Task {
                await viewModel.loadAccounts()
            }
        }
        .sheet(isPresented: $showingAddAccount) {
            AddAccountView()
        }
    }
}

struct AccountCard: View {
    let account: Account
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(account.name)
                    .font(.headline)
                
                Text(account.accountType.capitalized)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 4) {
                Text(formatCurrency(account.balance))
                    .font(.title3)
                    .bold()
                
                if account.isActive {
                    Text("Active")
                        .font(.caption)
                        .foregroundColor(.green)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
    
    private func formatCurrency(_ value: Decimal) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        return formatter.string(from: value as NSDecimalNumber) ?? "$0.00"
    }
}

struct AddAccountView: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            Form {
                Section("Account Information") {
                    Text("Add account form")
                }
            }
            .navigationTitle("Add Account")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        // TODO: Save account
                        dismiss()
                    }
                }
            }
        }
    }
}

@MainActor
class AccountsViewModel: ObservableObject {
    @Published var accounts: [Account] = []
    @Published var isLoading = false
    
    private let apiService = APIService()
    
    func loadAccounts() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            // TODO: Replace with actual user ID from auth
            accounts = try await apiService.fetchAccounts(userId: 1)
        } catch {
            print("Error loading accounts: \(error)")
        }
    }
}
