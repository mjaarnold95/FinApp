import Foundation
import Combine

class APIService: ObservableObject {
    private let baseURL: String
    private let session: URLSession
    
    init(baseURL: String = "http://localhost:8000") {
        self.baseURL = baseURL
        
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 300
        self.session = URLSession(configuration: config)
    }
    
    // MARK: - Generic Request
    private func request<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: Data? = nil
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)/api/v1/\(endpoint)") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = body
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw URLError(.badServerResponse)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(T.self, from: data)
    }
    
    // MARK: - Accounts
    func fetchAccounts(userId: Int) async throws -> [Account] {
        return try await request(endpoint: "accounts?user_id=\(userId)")
    }
    
    func createAccount(_ account: Account) async throws -> Account {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try encoder.encode(account)
        return try await request(endpoint: "accounts", method: "POST", body: data)
    }
    
    // MARK: - Transactions
    func fetchTransactions(userId: Int? = nil, accountId: Int? = nil) async throws -> [Transaction] {
        var endpoint = "transactions"
        var params: [String] = []
        
        if let userId = userId {
            params.append("user_id=\(userId)")
        }
        if let accountId = accountId {
            params.append("account_id=\(accountId)")
        }
        
        if !params.isEmpty {
            endpoint += "?" + params.joined(separator: "&")
        }
        
        return try await request(endpoint: endpoint)
    }
    
    func createTransaction(_ transaction: Transaction) async throws -> Transaction {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try encoder.encode(transaction)
        return try await request(endpoint: "transactions", method: "POST", body: data)
    }
    
    // MARK: - Investments
    func fetchInvestments(userId: Int) async throws -> [Investment] {
        return try await request(endpoint: "investments?user_id=\(userId)")
    }
    
    // MARK: - Dashboard Stats
    func fetchDashboardStats(userId: Int) async throws -> DashboardStats {
        return try await request(endpoint: "dashboard/stats?user_id=\(userId)")
    }
    
    // MARK: - Health Check
    func checkHealth() async throws -> Bool {
        let url = URL(string: "\(baseURL)/health")!
        let (_, response) = try await session.data(from: url)
        return (response as? HTTPURLResponse)?.statusCode == 200
    }
}
