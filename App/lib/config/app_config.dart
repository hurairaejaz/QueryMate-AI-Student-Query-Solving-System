class AppConfig {
  // Android emulator -> 10.0.2.2
  // Real phone -> use your PC LAN IP like 192.168.10.5
  // iOS simulator -> localhost may work if same machine
  // static const String baseUrl = "http://10.0.2.2:8000";
  static const String baseUrl = "https://leverage-glazing-unheated.ngrok-free.dev";

  static const String loginUrl = "$baseUrl/auth/login";
  static const String submitQueryUrl = "$baseUrl/queries/submit";
  static const String notificationsUrl = "$baseUrl/app/notifications/";
  static const String queryHistoryUrl = "$baseUrl/queries/history";
}