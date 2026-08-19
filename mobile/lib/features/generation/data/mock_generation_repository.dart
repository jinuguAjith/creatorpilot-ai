import 'dart:async';
import 'dart:math';

import '../../../core/constants/app_constants.dart';
import '../../campaign/domain/campaign_request.dart';

class GenerationJob {
  final String id;
  final GenerationStatus status;
  final String? posterUrl;
  final String? videoUrl;
  final String? caption;
  final List<String>? hashtags;
  final String? cta;
  final String? errorMessage;

  const GenerationJob({
    required this.id,
    required this.status,
    this.posterUrl,
    this.videoUrl,
    this.caption,
    this.hashtags,
    this.cta,
    this.errorMessage,
  });

  GenerationJob copyWith({GenerationStatus? status, String? errorMessage}) => GenerationJob(
        id: id,
        status: status ?? this.status,
        posterUrl: posterUrl,
        videoUrl: videoUrl,
        caption: caption,
        hashtags: hashtags,
        cta: cta,
        errorMessage: errorMessage ?? this.errorMessage,
      );
}

/// MOCK ONLY. Real implementation (Phase 4+) calls:
///   POST /v1/campaigns            -> { jobId }
///   GET  /v1/generations/{jobId}  -> polls status, or use FCM/websocket push
/// The backend — never this app — talks to Gemini/Veo/TTS and FFmpeg.
/// This mock exists so UI, navigation, and progress states can be built
/// and tested before the real orchestrator (Phase 4) exists.
class MockGenerationRepository {
  final _rng = Random();

  Future<String> submitCampaign(CampaignRequest request) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return 'job_${_rng.nextInt(999999)}';
  }

  /// Emits the full REQUESTED -> QUEUED -> ... -> COMPLETED lifecycle.
  /// Real version replaces this with server-sent status polling.
  Stream<GenerationJob> watchJob(String jobId) async* {
    const stages = [
      GenerationStatus.requested,
      GenerationStatus.queued,
      GenerationStatus.processing,
      GenerationStatus.generating,
      GenerationStatus.composing,
      GenerationStatus.completed,
    ];
    for (final stage in stages) {
      await Future.delayed(const Duration(milliseconds: 900));
      if (stage == GenerationStatus.completed) {
        yield GenerationJob(
          id: jobId,
          status: stage,
          posterUrl: 'https://picsum.photos/seed/$jobId/1080/1350',
          caption: 'Grand opening this Sunday — 20% off for early birds! ✨',
          hashtags: const ['#GrandOpening', '#ItalianCuisine', '#Bangalore'],
          cta: 'Reserve your table today',
        );
      } else {
        yield GenerationJob(id: jobId, status: stage);
      }
    }
  }
}
