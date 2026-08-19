import '../../../core/constants/app_constants.dart';

/// What the mobile app sends to the backend. The backend — never the app —
/// decides how this maps to AI provider calls, so no provider/model name
/// appears here.
class CampaignRequest {
  final String description;
  final String industry;
  final String language;
  final String style;
  final String targetAudience;
  final String offerDetails;
  final String location;
  final String aspectRatio;
  final Set<OutputType> outputs;
  final String? voiceoverLanguage;

  const CampaignRequest({
    required this.description,
    required this.industry,
    required this.language,
    required this.style,
    required this.targetAudience,
    required this.offerDetails,
    required this.location,
    required this.aspectRatio,
    required this.outputs,
    this.voiceoverLanguage,
  });

  Map<String, dynamic> toJson() => {
        'description': description,
        'industry': industry,
        'language': language,
        'style': style,
        'target_audience': targetAudience,
        'offer_details': offerDetails,
        'location': location,
        'aspect_ratio': aspectRatio,
        'outputs': outputs.map((o) => o.name).toList(),
        if (voiceoverLanguage != null) 'voiceover_language': voiceoverLanguage,
      };
}
