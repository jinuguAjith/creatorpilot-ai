import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import 'package:video_player/video_player.dart';
import '../data/generation_repository.dart';

class GenerationResultScreen extends StatefulWidget {
  final String jobId;
  const GenerationResultScreen({super.key, required this.jobId});

  @override
  State<GenerationResultScreen> createState() => _GenerationResultScreenState();
}

class _GenerationResultScreenState extends State<GenerationResultScreen> {
  final _repo = GenerationRepository();
  GenerationJob? _job;
  VideoPlayerController? _video;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final job = await _repo.getJob(widget.jobId);
    if (!mounted) return;
    setState(() => _job = job);

    if (job.videoUrl != null) {
      final controller =
          VideoPlayerController.networkUrl(Uri.parse(job.videoUrl!));
      await controller.initialize();
      controller.setLooping(true);
      if (!mounted) {
        controller.dispose();
        return;
      }
      setState(() => _video = controller);
    }
  }

  @override
  void dispose() {
    _video?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final job = _job;
    if (job == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Your Campaign')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          if (job.posterUrl != null)
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: CachedNetworkImage(imageUrl: job.posterUrl!),
            ),
          if (_video != null) ...[
            const SizedBox(height: 20),
            const Text('Social Video',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: AspectRatio(
                aspectRatio: _video!.value.aspectRatio,
                child: VideoPlayer(_video!),
              ),
            ),
            IconButton.filled(
              onPressed: () {
                _video!.value.isPlaying ? _video!.pause() : _video!.play();
                setState(() {});
              },
              icon: Icon(
                _video!.value.isPlaying ? Icons.pause : Icons.play_arrow,
              ),
            ),
          ],
          if (job.caption != null) ...[
            const SizedBox(height: 20),
            Text(job.caption!),
          ],
          if (job.hashtags != null)
            Wrap(
              spacing: 6,
              children: job.hashtags!.map((h) => Chip(label: Text(h))).toList(),
            ),
          const SizedBox(height: 20),
          Row(
            children: [
              if (job.posterUrl != null)
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => Share.share(job.posterUrl!),
                    icon: const Icon(Icons.share),
                    label: const Text('Share Poster'),
                  ),
                ),
              if (job.videoUrl != null) ...[
                const SizedBox(width: 10),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => Share.share(job.videoUrl!),
                    icon: const Icon(Icons.movie),
                    label: const Text('Share Video'),
                  ),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}
