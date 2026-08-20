import 'dart:async';
import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../core/constants/api_config.dart';
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

  factory GenerationJob.fromJson(Map<String, dynamic> json) {
    final status = switch (json['status'] as String?) {
      'REQUESTED' => GenerationStatus.requested,
      'QUEUED' => GenerationStatus.queued,
      'PROCESSING' => GenerationStatus.processing,
      'GENERATING' => GenerationStatus.generating,
      'COMPOSING' => GenerationStatus.composing,
      'COMPLETED' => GenerationStatus.completed,
      'FAILED' => GenerationStatus.failed,
      _ => GenerationStatus.failed,
    };

    return GenerationJob(
      id: json['job_id'] as String,
      status: status,
      posterUrl: json['poster_url'] as String?,
      videoUrl: json['video_url'] as String?,
      caption: json['caption'] as String?,
      hashtags: (json['hashtags'] as List?)?.cast<String>(),
      cta: json['cta'] as String?,
      errorMessage: json['error_message'] as String?,
    );
  }
}

class GenerationRepository {
  GenerationRepository({Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: ApiConfig.baseUrl,
                connectTimeout: const Duration(seconds: 20),
                receiveTimeout: const Duration(seconds: 30),
              ),
            );

  final Dio _dio;

  Future<Options> _authOptions() async {
    final token = await FirebaseAuth.instance.currentUser?.getIdToken();
    return Options(headers: {
      if (token != null) 'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    });
  }

  Future<String> submitCampaign(CampaignRequest request) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/v1/campaigns',
      data: request.toJson(),
      options: await _authOptions(),
    );
    return response.data!['job_id'] as String;
  }

  Future<GenerationJob> getJob(String jobId) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/v1/generations/$jobId',
      options: await _authOptions(),
    );
    return GenerationJob.fromJson(response.data!);
  }

  Stream<GenerationJob> watchJob(
    String jobId, {
    Duration interval = const Duration(seconds: 4),
  }) async* {
    while (true) {
      final job = await getJob(jobId);
      yield job;
      if (job.status == GenerationStatus.completed ||
          job.status == GenerationStatus.failed) {
        return;
      }
      await Future<void>.delayed(interval);
    }
  }
}
