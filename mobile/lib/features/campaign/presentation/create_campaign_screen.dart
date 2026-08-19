import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_constants.dart';
import '../../generation/data/mock_generation_repository.dart';
import '../domain/campaign_request.dart';

class CreateCampaignScreen extends StatefulWidget {
  const CreateCampaignScreen({super.key});

  @override
  State<CreateCampaignScreen> createState() => _CreateCampaignScreenState();
}

class _CreateCampaignScreenState extends State<CreateCampaignScreen> {
  final _descriptionCtrl = TextEditingController();
  final _industryCtrl = TextEditingController();
  final _audienceCtrl = TextEditingController();
  final _offerCtrl = TextEditingController();
  final _locationCtrl = TextEditingController();

  String _language = 'English';
  String _style = AppConstants.styles.first;
  String _aspectRatio = AppConstants.aspectRatios.first;
  final Set<OutputType> _outputs = {OutputType.poster, OutputType.video, OutputType.caption};
  bool _submitting = false;

  final _repo = MockGenerationRepository(); // Phase 4: inject real repository

  Future<void> _generate() async {
    if (_descriptionCtrl.text.trim().isEmpty || _outputs.isEmpty) return;
    setState(() => _submitting = true);

    final request = CampaignRequest(
      description: _descriptionCtrl.text.trim(),
      industry: _industryCtrl.text.trim(),
      language: _language,
      style: _style,
      targetAudience: _audienceCtrl.text.trim(),
      offerDetails: _offerCtrl.text.trim(),
      location: _locationCtrl.text.trim(),
      aspectRatio: _aspectRatio,
      outputs: _outputs,
      voiceoverLanguage: _outputs.contains(OutputType.voiceover) ? 'English' : null,
    );

    // Real flow: backend checks + reserves credits BEFORE returning jobId.
    // If insufficient credits, backend returns 402 and UI routes to /credits.
    final jobId = await _repo.submitCampaign(request);
    if (mounted) context.push('/generation/$jobId/status');
    if (mounted) setState(() => _submitting = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New Campaign')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const _SectionLabel('What are you promoting?'),
            TextField(
              controller: _descriptionCtrl,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText:
                    'e.g. Grand opening of Bella Aroma restaurant this Sunday in Bangalore, 20% opening offer, luxury Italian, for couples and families.',
              ),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _industryCtrl,
                    decoration: const InputDecoration(labelText: 'Industry'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _locationCtrl,
                    decoration: const InputDecoration(labelText: 'Location'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _audienceCtrl,
              decoration: const InputDecoration(labelText: 'Target audience'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _offerCtrl,
              decoration: const InputDecoration(labelText: 'Offer / details'),
            ),
            const SizedBox(height: 24),
            const _SectionLabel('Style'),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: AppConstants.styles.map((s) {
                final selected = s == _style;
                return ChoiceChip(
                  label: Text(s),
                  selected: selected,
                  onSelected: (_) => setState(() => _style = s),
                );
              }).toList(),
            ),
            const SizedBox(height: 24),
            const _SectionLabel('Aspect ratio'),
            Wrap(
              spacing: 8,
              children: AppConstants.aspectRatios.map((r) {
                final selected = r == _aspectRatio;
                return ChoiceChip(
                  label: Text(r),
                  selected: selected,
                  onSelected: (_) => setState(() => _aspectRatio = r),
                );
              }).toList(),
            ),
            const SizedBox(height: 24),
            const _SectionLabel('What should we generate?'),
            _OutputToggle(
              outputs: _outputs,
              type: OutputType.poster,
              label: 'Poster',
              credits: AppConstants.posterCredits,
              onChanged: (v) => setState(() => v ? _outputs.add(OutputType.poster) : _outputs.remove(OutputType.poster)),
            ),
            _OutputToggle(
              outputs: _outputs,
              type: OutputType.video,
              label: 'Video (30s)',
              credits: AppConstants.video30SecCredits,
              onChanged: (v) => setState(() => v ? _outputs.add(OutputType.video) : _outputs.remove(OutputType.video)),
            ),
            _OutputToggle(
              outputs: _outputs,
              type: OutputType.caption,
              label: 'Caption + hashtags',
              credits: 0,
              onChanged: (v) => setState(() => v ? _outputs.add(OutputType.caption) : _outputs.remove(OutputType.caption)),
            ),
            _OutputToggle(
              outputs: _outputs,
              type: OutputType.voiceover,
              label: 'Voice-over',
              credits: AppConstants.voiceoverCredits,
              onChanged: (v) => setState(() => v ? _outputs.add(OutputType.voiceover) : _outputs.remove(OutputType.voiceover)),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _submitting ? null : _generate,
              child: _submitting
                  ? const SizedBox(
                      height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Text('Generate'),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  final String text;
  const _SectionLabel(this.text);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Text(text, style: Theme.of(context).textTheme.titleSmall),
    );
  }
}

class _OutputToggle extends StatelessWidget {
  final Set<OutputType> outputs;
  final OutputType type;
  final String label;
  final int credits;
  final ValueChanged<bool> onChanged;

  const _OutputToggle({
    required this.outputs,
    required this.type,
    required this.label,
    required this.credits,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      contentPadding: EdgeInsets.zero,
      value: outputs.contains(type),
      onChanged: onChanged,
      title: Text(label),
      subtitle: credits > 0 ? Text('$credits credits') : null,
    );
  }
}
