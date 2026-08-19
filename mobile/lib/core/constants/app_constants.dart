/// Central, non-hardcoded configuration for product-facing constants.
/// Credit costs mirror `backend/config/credit_config.json` — the backend
/// is the source of truth; this copy is only used for optimistic UI display.
class AppConstants {
  AppConstants._();

  static const String appName = 'CreatorPilot AI';
  static const String tagline = 'One Idea. Complete Content.';

  // Display-only credit costs (backend re-validates on every request).
  static const int posterCredits = 5;
  static const int video30SecCredits = 25;
  static const int video60SecCredits = 45;
  static const int voiceoverCredits = 8;
  static const int regenerateCredits = 5;

  static const List<String> styles = [
    'Luxury',
    'Modern',
    'Cinematic',
    'Minimal',
    'Energetic',
    'Professional',
    'Festival',
    'Elegant',
  ];

  static const List<String> aspectRatios = ['9:16', '1:1', '4:5', '16:9'];

  static const List<String> voiceoverLanguages = [
    'English',
    'Telugu',
    'Hindi',
    'Tamil',
    'Kannada',
  ];

  static const List<String> audioMoods = [
    'Cinematic',
    'Luxury',
    'Emotional',
    'Energetic',
    'Corporate',
    'Inspirational',
    'Restaurant',
    'Festival',
  ];
}

enum OutputType { poster, video, caption, voiceover }

enum GenerationStatus {
  requested,
  queued,
  processing,
  generating,
  composing,
  completed,
  failed,
}
