import Foundation
import Combine
import AppKit
import UserNotifications
import ServiceManagement

struct Preset: Codable, Identifiable, Equatable {
    var id = UUID()
    var name: String
    var seconds: TimeInterval
}

enum TimerState: Equatable {
    case idle, running, paused
}

final class TimerManager: ObservableObject {
    @Published private(set) var state: TimerState = .idle
    @Published private(set) var remaining: TimeInterval = 0
    @Published var inputString = ""
    @Published var errorMessage: String?
    @Published var presets: [Preset] {
        didSet { savePresets() }
    }
    @Published var launchAtLogin: Bool {
        didSet { updateLaunchAtLogin() }
    }

    private var endDate: Date?
    private var ticker: AnyCancellable?
    private var totalDuration: TimeInterval = 0
    private let defaults = UserDefaults.standard
    private let presetsKey = "presets"

    init() {
        if let data = defaults.data(forKey: presetsKey),
           let decoded = try? JSONDecoder().decode([Preset].self, from: data) {
            presets = decoded
        } else {
            presets = [
                Preset(name: "Pomodoro", seconds: 25 * 60),
                Preset(name: "Short break", seconds: 5 * 60),
                Preset(name: "Tea", seconds: 4 * 60)
            ]
        }
        launchAtLogin = SMAppService.mainApp.status == .enabled
    }

    // MARK: - Derived values

    var progress: Double {
        totalDuration > 0 ? min(1, max(0, 1 - remaining / totalDuration)) : 0
    }

    var displayString: String {
        Self.format(remaining)
    }

    var menuBarTitle: String {
        switch state {
        case .idle: return "⏱"
        case .running: return displayString
        case .paused: return "⏸ " + displayString
        }
    }

    // MARK: - Controls

    func startFromText() {
        guard let seconds = Self.parse(inputString) else {
            errorMessage = "Try 1h 25m, 90, 1.5h, or 1:30"
            return
        }
        start(seconds: seconds)
    }

    func start(seconds: TimeInterval) {
        guard seconds > 0 else {
            errorMessage = "Enter a duration above zero"
            return
        }
        errorMessage = nil
        totalDuration = seconds
        remaining = seconds
        endDate = Date().addingTimeInterval(seconds)
        state = .running
        startTicker()
    }

    func togglePause() {
        switch state {
        case .running:
            remaining = max(0, endDate?.timeIntervalSinceNow ?? 0)
            endDate = nil
            ticker?.cancel()
            state = .paused
        case .paused:
            endDate = Date().addingTimeInterval(remaining)
            state = .running
            startTicker()
        case .idle:
            break
        }
    }

    func addTime(_ seconds: TimeInterval) {
        guard state != .idle else { return }
        totalDuration += seconds
        if state == .running, let endDate {
            self.endDate = endDate.addingTimeInterval(seconds)
        } else {
            remaining += seconds
        }
    }

    func stop() {
        ticker?.cancel()
        ticker = nil
        endDate = nil
        totalDuration = 0
        remaining = 0
        state = .idle
        NSApp.dockTile.badgeLabel = nil
    }

    // MARK: - Presets

    func savePreset(name: String, seconds: TimeInterval) {
        presets.append(Preset(name: name, seconds: seconds))
    }

    func removePreset(_ preset: Preset) {
        presets.removeAll { $0.id == preset.id }
    }

    private func savePresets() {
        if let data = try? JSONEncoder().encode(presets) {
            defaults.set(data, forKey: presetsKey)
        }
    }

    // MARK: - Ticking

    private func startTicker() {
        ticker?.cancel()
        ticker = Timer.publish(every: 0.2, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] now in self?.tick(now) }
    }

    private func tick(_ now: Date) {
        guard state == .running, let endDate else { return }
        remaining = max(0, endDate.timeIntervalSince(now))
        NSApp.dockTile.badgeLabel = displayString
        if remaining == 0 {
            finish()
        }
    }

    private func finish() {
        stop()
        NSSound(named: "Glass")?.play()

        let content = UNMutableNotificationContent()
        content.title = "Time's up"
        content.body = "Your timer finished."
        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil
        )
        UNUserNotificationCenter.current().add(request)
    }

    // MARK: - Launch at login

    private func updateLaunchAtLogin() {
        do {
            if launchAtLogin {
                try SMAppService.mainApp.register()
            } else {
                try SMAppService.mainApp.unregister()
            }
        } catch {
            errorMessage = "Couldn't change launch at login"
        }
    }

    // MARK: - Formatting and parsing

    static func format(_ seconds: TimeInterval) -> String {
        let total = Int(ceil(seconds))
        let h = total / 3600
        let m = (total % 3600) / 60
        let s = total % 60
        return h > 0
            ? String(format: "%d:%02d:%02d", h, m, s)
            : String(format: "%02d:%02d", m, s)
    }

    /// Accepts "1h 25m 10s", "1h25m", "1.5h", "90" (minutes), "1:30" (m:ss), "1:30:00" (h:mm:ss).
    static func parse(_ input: String) -> TimeInterval? {
        let text = input.lowercased().trimmingCharacters(in: .whitespaces)
        guard !text.isEmpty else { return nil }

        if let minutes = Double(text) {
            return minutes * 60
        }

        if text.contains(":") {
            let rawParts = text.split(separator: ":", omittingEmptySubsequences: false)
            let values = rawParts.compactMap { Double($0) }
            guard values.count == rawParts.count else { return nil }
            switch values.count {
            case 2: return values[0] * 60 + values[1]
            case 3: return values[0] * 3600 + values[1] * 60 + values[2]
            default: return nil
            }
        }

        guard let regex = try? NSRegularExpression(pattern: #"(\d+(?:\.\d+)?)\s*(h|m|s)"#) else {
            return nil
        }
        let ns = text as NSString
        let matches = regex.matches(in: text, range: NSRange(location: 0, length: ns.length))
        guard !matches.isEmpty else { return nil }

        var total: TimeInterval = 0
        for match in matches {
            let value = Double(ns.substring(with: match.range(at: 1))) ?? 0
            switch ns.substring(with: match.range(at: 2)) {
            case "h": total += value * 3600
            case "m": total += value * 60
            default:  total += value
            }
        }
        return total > 0 ? total : nil
    }
}
