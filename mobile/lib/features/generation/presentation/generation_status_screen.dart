import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/theme/app_theme.dart';
import '../data/mock_generation_repository.dart';

const _stageLabels = {
  GenerationStatus.requested: 'Understanding your idea',
  GenerationStatus.queued: 'Queued for generation',
  GenerationStatus.processing: 'Writing your campaign strategy',
  GenerationStatus.generating: 'Creating visuals & video scenes',
  GenerationStatus.composing: 'Composing final video',
  GenerationStatus.completed: 'Done',
  GenerationStatus.failed: 'Failed',
};

class GenerationStatusScreen extends StatefulWidget {
  final String jobId;
  const GenerationStatusScreen({super.key, required this.jobId});

  @override
  State<GenerationStatusScreen> createState() => _GenerationStatusScreenState();
}

class _GenerationStatusScreenState extends State<GenerationStatusScreen> {
  final _repo = MockGenerationRepository(); // Phase 4: inject real repository
  GenerationStatus _status = GenerationStatus.requested;

  @override
  void initState() {
    super.initState();
    _repo.watchJob(widget.jobId).listen((job) {
      if (!mounted) return;
      setState(() => _status = job.status);
      if (job.status == GenerationStatus.completed) {
        context.pushReplacement('/generation/${widget.jobId}/result');
      }
      if (job.status == GenerationStatus.failed) {
        _showFailureSheet();
      }
    });
  }

  void _showFailureSheet() {
    showModalBottomSheet(
      context: context,
      builder: (_) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Your content could not be generated this time.',
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
            const SizedBox(height: 8),
            const Text(
              'Any credits reserved for this job have been refunded.',
              style: TextStyle(color: AppColors.textSecondary),
            ),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: () => context.pop(), child: const Text('Try Again')),
            const SizedBox(height: 8),
            OutlinedButton(onPressed: () => context.pop(), child: const Text('Contact Support')),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 24),
                Text(
                  _stageLabels[_status] ?? '',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                const Text(
                  "We'll notify you the moment it's ready. Feel free to leave this screen.",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
