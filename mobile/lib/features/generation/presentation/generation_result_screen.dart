import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

import '../../../core/theme/app_theme.dart';

class GenerationResultScreen extends StatelessWidget {
  final String jobId;
  const GenerationResultScreen({super.key, required this.jobId});

  @override
  Widget build(BuildContext context) {
    // Phase 8: load the real GenerationJob (poster/video URLs, caption,
    // hashtags, CTA) from Firestore via ProjectsRepository using jobId.
    final posterUrl = 'https://picsum.photos/seed/$jobId/1080/1350';
    const caption = 'Grand opening this Sunday — 20% off for early birds! ✨';
    const hashtags = ['#GrandOpening', '#ItalianCuisine', '#Bangalore'];
    const cta = 'Reserve your table today';

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Campaign'),
        actions: [
          IconButton(
            icon: const Icon(Icons.flag_outlined),
            tooltip: 'Report AI Output',
            onPressed: () => _showReportSheet(context),
          ),
        ],
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: AspectRatio(
                aspectRatio: 4 / 5,
                child: CachedNetworkImage(imageUrl: posterUrl, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 20),
            Text(caption, style: Theme.of(context).textTheme.bodyLarge),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: hashtags
                  .map((h) => Chip(label: Text(h), backgroundColor: AppColors.surfaceCard))
                  .toList(),
            ),
            const SizedBox(height: 12),
            Text('CTA: $cta', style: const TextStyle(color: AppColors.accent)),
            const SizedBox(height: 28),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.download_outlined),
                    label: const Text('Download'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.share_outlined),
                    label: const Text('Share'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.refresh),
              label: const Text('Regenerate'),
            ),
          ],
        ),
      ),
    );
  }

  void _showReportSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (_) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Report this AI output', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            const Text(
              'Tell us what looks wrong. Reports are reviewed by our safety team.',
              style: TextStyle(color: AppColors.textSecondary),
            ),
            const SizedBox(height: 16),
            TextField(
              maxLines: 3,
              decoration: const InputDecoration(hintText: 'What went wrong?'),
            ),
            const SizedBox(height: 16),
            // Phase 15: POST /v1/reports { jobId, reason } to backend.
            ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text('Submit Report')),
          ],
        ),
      ),
    );
  }
}
