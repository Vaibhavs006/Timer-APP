import SwiftUI
import UserNotifications

@main
struct SmartQuickTimerApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    @StateObject private var manager = TimerManager()

    var body: some Scene {
        Window("Smart Quick Timer", id: "main") {
            TimerView(manager: manager)
        }
        .defaultSize(width: 420, height: 560)
        .windowResizability(.contentSize)

        MenuBarExtra {
            TimerView(manager: manager, compact: true)
        } label: {
            Text(manager.menuBarTitle)
                .monospacedDigit()
        }
        .menuBarExtraStyle(.window)
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        let center = UNUserNotificationCenter.current()
        center.delegate = self
        center.requestAuthorization(options: [.alert]) { _, _ in }
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        false
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        completionHandler([.banner])
    }
}

struct TimerView: View {
    @ObservedObject var manager: TimerManager
    var compact = false

    @Environment(\.openWindow) private var openWindow
    @State private var presetName = ""
    @State private var showingSave = false

    var body: some View {
        VStack(alignment: .leading, spacing: compact ? 12 : 18) {
            if manager.state == .idle {
                inputSection
            } else {
                runningSection
            }

            if let error = manager.errorMessage {
                Text(error)
                    .font(.caption)
                    .foregroundStyle(.red)
            }

            presetsSection

            Divider()
            footer
        }
        .padding(compact ? 12 : 20)
        .frame(width: compact ? 270 : 420)
    }

    private var inputSection: some View {
        HStack {
            TextField("1h 25m, 90, 1:30:00", text: $manager.inputString)
                .textFieldStyle(.roundedBorder)
                .onSubmit { manager.startFromText() }
            Button("Start") { manager.startFromText() }
                .buttonStyle(.borderedProminent)
        }
    }

    private var runningSection: some View {
        VStack(spacing: 10) {
            ZStack {
                Circle()
                    .stroke(.quaternary, lineWidth: 8)
                Circle()
                    .trim(from: 0, to: manager.progress)
                    .stroke(.tint, style: StrokeStyle(lineWidth: 8, lineCap: .round))
                    .rotationEffect(.degrees(-90))
                    .animation(.linear(duration: 0.2), value: manager.progress)
                Text(manager.displayString)
                    .font(.system(size: compact ? 24 : 40, weight: .semibold, design: .rounded))
                    .monospacedDigit()
            }
            .frame(width: compact ? 130 : 200, height: compact ? 130 : 200)

            HStack {
                Button(manager.state == .paused ? "Resume" : "Pause") {
                    manager.togglePause()
                }
                .keyboardShortcut("p", modifiers: .command)

                Button("+1 min") { manager.addTime(60) }

                Button("Stop", role: .destructive) { manager.stop() }
            }
            .buttonStyle(.bordered)
        }
        .frame(maxWidth: .infinity)
    }

    private var presetsSection: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text("Presets")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Spacer()
                if manager.state == .idle {
                    Button("Save current") { showingSave = true }
                        .font(.caption)
                        .disabled(TimerManager.parse(manager.inputString) == nil)
                        .popover(isPresented: $showingSave) { savePopover }
                }
            }

            ForEach(manager.presets) { preset in
                HStack {
                    Button(preset.name) { manager.start(seconds: preset.seconds) }
                        .buttonStyle(.plain)
                    Spacer()
                    Text(TimerManager.format(preset.seconds))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .monospacedDigit()
                    Button {
                        manager.removePreset(preset)
                    } label: {
                        Image(systemName: "minus.circle")
                    }
                    .buttonStyle(.borderless)
                    .foregroundStyle(.secondary)
                }
            }
        }
    }

    private var savePopover: some View {
        VStack(alignment: .leading, spacing: 8) {
            TextField("Name (optional)", text: $presetName)
                .textFieldStyle(.roundedBorder)
            Button("Save") {
                if let seconds = TimerManager.parse(manager.inputString) {
                    let name = presetName.isEmpty ? TimerManager.format(seconds) : presetName
                    manager.savePreset(name: name, seconds: seconds)
                }
                presetName = ""
                showingSave = false
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
        .frame(width: 220)
    }

    private var footer: some View {
        HStack {
            if compact {
                Button("Open window") {
                    openWindow(id: "main")
                    NSApp.activate(ignoringOtherApps: true)
                }
            } else {
                Toggle("Launch at login", isOn: $manager.launchAtLogin)
                    .toggleStyle(.checkbox)
            }
            Spacer()
            Button("Quit") { NSApp.terminate(nil) }
        }
        .font(.caption)
    }
}
