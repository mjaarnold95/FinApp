# FinApp - Native iOS & macOS Apps

Native applications for iOS and macOS built with SwiftUI, providing seamless synchronization with the web application.

## Features

- **Universal App**: Single codebase runs on both iOS and macOS
- **Real-time Sync**: WebSocket-based synchronization across all platforms
- **Offline Support**: Local data caching with automatic sync when online
- **Native UI**: Platform-specific interfaces optimized for iOS and macOS
- **Secure**: Token-based authentication with encrypted data storage

## Architecture

### SwiftUI Components

- **FinAppApp.swift**: Main app entry point
- **ContentView.swift**: Adaptive layout for iOS (TabView) and macOS (NavigationSplitView)
- **Views**: Dashboard, Accounts, Transactions, Investments, Payroll, Retirement, Taxes
- **Services**: API client and sync service for real-time updates

### Synchronization

The app uses two sync mechanisms:

1. **WebSocket** (Primary): Real-time bidirectional communication
   - Connects to `ws://localhost:8000/ws/sync/{user_id}`
   - Receives instant notifications when data changes
   - Ideal for active sessions

2. **Polling** (Fallback): HTTP-based periodic sync
   - Polls every 30 seconds for changes
   - Ensures sync even when WebSocket is unavailable
   - Lightweight health checks

## Requirements

### iOS
- iOS 16.0 or later
- iPhone or iPad

### macOS
- macOS 13.0 (Ventura) or later
- Apple Silicon or Intel Mac

## Building & Running

### Xcode

1. Open `FinApp.xcodeproj` in Xcode
2. Select your target (iOS or macOS)
3. Build and run (⌘R)

### Command Line

```bash
# Build for iOS Simulator
xcodebuild -project FinApp.xcodeproj -scheme FinApp-iOS -destination 'platform=iOS Simulator,name=iPhone 15' build

# Build for macOS
xcodebuild -project FinApp.xcodeproj -scheme FinApp-macOS -destination 'platform=macOS' build
```

## Configuration

### API Endpoint

The app connects to the backend API at `http://localhost:8000` by default. To change this:

1. Open `APIService.swift`
2. Modify the `baseURL` parameter in the initializer:

```swift
init(baseURL: String = "https://your-api-domain.com") {
    self.baseURL = baseURL
    // ...
}
```

### Sync Settings

Adjust sync frequency in `SyncService.swift`:

```swift
// Change polling interval (in seconds)
syncTimer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { ... }
```

## Data Models

The app includes Swift models matching the backend schema:

- **User**: User profile and authentication
- **Account**: Financial accounts (checking, savings, etc.)
- **Transaction**: Income and expense transactions
- **Investment**: Investment portfolio holdings
- **DashboardStats**: Aggregated financial statistics

All models conform to `Codable` for JSON serialization and `Identifiable` for SwiftUI lists.

## Sync Flow

### Creating a Transaction

1. User creates transaction in iOS app
2. App sends POST request to `/api/v1/transactions`
3. Backend creates transaction and ledger entries
4. Backend broadcasts WebSocket message to all connected clients
5. macOS and web apps receive notification and refresh data
6. All apps display the new transaction

### Cross-Platform Consistency

- All apps connect to the same backend API
- WebSocket ensures real-time updates across devices
- Optimistic UI updates with server validation
- Conflict resolution handled server-side

## Platform-Specific Features

### iOS

- **Tab Navigation**: Bottom tab bar for main sections
- **Touch Optimized**: Large touch targets and gestures
- **Mobile Patterns**: Pull-to-refresh, swipe actions

### macOS

- **Sidebar Navigation**: Left sidebar with all sections
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Window Management**: Resizable windows with toolbars

## Security

- **HTTPS Only** (in production)
- **Token Authentication**: Secure JWT-based auth
- **Keychain Storage**: Credentials stored in system keychain
- **Certificate Pinning**: Optional SSL pinning for enhanced security

## Testing

### Unit Tests

```bash
xcodebuild test -project FinApp.xcodeproj -scheme FinApp-iOS -destination 'platform=iOS Simulator,name=iPhone 15'
```

### UI Tests

```bash
xcodebuild test -project FinApp.xcodeproj -scheme FinApp-macOS -destination 'platform=macOS'
```

## Deployment

### iOS App Store

1. Archive the app in Xcode
2. Upload to App Store Connect
3. Submit for review

### macOS App Store

1. Archive the app in Xcode
2. Notarize the app with Apple
3. Upload to App Store Connect
4. Submit for review

### Direct Distribution (macOS)

1. Archive the app
2. Export as macOS app
3. Notarize with Apple
4. Distribute DMG file

## Future Enhancements

- [ ] Face ID / Touch ID authentication
- [ ] Widgets for iOS 14+ and macOS
- [ ] Siri shortcuts integration
- [ ] Apple Watch companion app
- [ ] iCloud sync for offline changes
- [ ] Dark mode support (system adaptive)
- [ ] Localization for multiple languages

## Support

For issues or questions:
- Check the main README in the root directory
- Review backend API documentation at `/docs`
- Ensure backend is running on `http://localhost:8000`

## License

Same license as the main FinApp project (see root LICENSE file).
