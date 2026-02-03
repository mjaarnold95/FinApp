import Foundation

// MARK: - User
struct User: Codable, Identifiable {
    let id: Int
    let email: String
    let username: String
    let firstName: String
    let lastName: String
    let isActive: Bool
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, email, username
        case firstName = "first_name"
        case lastName = "last_name"
        case isActive = "is_active"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Account
struct Account: Codable, Identifiable {
    let id: Int
    let userId: Int
    let institutionId: Int?
    let name: String
    let accountType: String
    let accountNumber: String?
    let balance: Decimal
    let currency: String
    let isActive: Bool
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, name, balance, currency
        case userId = "user_id"
        case institutionId = "institution_id"
        case accountType = "account_type"
        case accountNumber = "account_number"
        case isActive = "is_active"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Transaction
struct Transaction: Codable, Identifiable {
    let id: Int
    let userId: Int
    let accountId: Int
    let transactionDate: Date
    let description: String
    let amount: Decimal
    let category: String?
    let merchant: String?
    let notes: String?
    let isRecurring: Bool
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, description, amount, category, merchant, notes
        case userId = "user_id"
        case accountId = "account_id"
        case transactionDate = "transaction_date"
        case isRecurring = "is_recurring"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Investment
struct Investment: Codable, Identifiable {
    let id: Int
    let userId: Int
    let accountId: Int
    let investmentType: String
    let symbol: String
    let name: String
    let quantity: Decimal
    let purchasePrice: Decimal
    let currentPrice: Decimal
    let purchaseDate: Date
    let notes: String?
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, symbol, name, quantity, notes
        case userId = "user_id"
        case accountId = "account_id"
        case investmentType = "investment_type"
        case purchasePrice = "purchase_price"
        case currentPrice = "current_price"
        case purchaseDate = "purchase_date"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Dashboard Stats
struct DashboardStats: Codable {
    let totalBalance: Decimal
    let monthlyIncome: Decimal
    let monthlyExpenses: Decimal
    let investmentValue: Decimal
    
    enum CodingKeys: String, CodingKey {
        case totalBalance = "total_balance"
        case monthlyIncome = "monthly_income"
        case monthlyExpenses = "monthly_expenses"
        case investmentValue = "investment_value"
    }
}
