import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_constants.dart';
import '../../../core/theme/app_theme.dart';
import '../data/generation_repository.dart';

const _labels = {
  GenerationStatus.requested: 'Understanding your idea',
  GenerationStatus.queued: 'Queued',
  GenerationStatus.processing: 'Building campaign strategy',
  GenerationStatus.generating: 'Creating premium poster and video',
  GenerationStatus.composing: 'Composing final video',
  GenerationStatus.completed: 'Done',
  GenerationStatus.failed: 'Generation failed',
};

class GenerationStatusScreen extends StatefulWidget {
  final String jobId;
  const GenerationStatusScreen({super.key, required this.jobId});

  @override
  State<GenerationStatusScreen> createState() => _GenerationStatusScreenState();
}

class _GenerationStatusScreenState extends State<GenerationStatusScreen> {
  final _repo = GenerationRepository();
  StreamSubscription<GenerationJob>? _subscription;
  GenerationStatus _status = GenerationStatus.requested;
  String? _error;

  @override
  void initState() {
    super.initState();
    _subscription = _repo.watchJob(widget.jobId).listen((job) {
      if (!mounted) return;
      setState(() {
        _status = job.status;
        _error = job.errorMessage;
      });
      if (job.status == GenerationStatus.completed) {
        context.pushReplacement('/generation/${widget.jobId}/result');
      } else if (job.status == GenerationStatus.failed) {
        _showFailure();
      }
    }, onError: (_) {
      if (mounted) setState(() => _error = 'Status check failed.');
    });
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }

  void _showFailure() {
    showModalBottomSheet(
      context: context,
      builder: (_) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Generation failed',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            Text(_error ?? 'Reserved credits have been refunded.',
                style: const TextStyle(color: AppColors.textSecondary)),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => context.pop(),
              child: const Text('Try Again'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 24),
                Text(_labels[_status] ?? 'Generating...',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 8),
                const Text(
                  'The server is creating your real AI assets. You can leave this screen.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
        ),
      );
}
