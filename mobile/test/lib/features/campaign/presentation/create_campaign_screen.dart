import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_constants.dart';
import '../../generation/data/generation_repository.dart';
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

  String _style = AppConstants.styles.first;
  String _aspectRatio = '4:5';
  final Set<OutputType> _outputs = {
    OutputType.poster,
    OutputType.video,
    OutputType.caption,
  };
  bool _submitting = false;

  final _repo = GenerationRepository();

  Future<void> _generate() async {
    if (_descriptionCtrl.text.trim().isEmpty) return;
    setState(() => _submitting = true);

    try {
      final request = CampaignRequest(
        description: _descriptionCtrl.text.trim(),
        industry: _industryCtrl.text.trim(),
        language: 'English',
        style: _style,
        targetAudience: _audienceCtrl.text.trim(),
        offerDetails: _offerCtrl.text.trim(),
        location: _locationCtrl.text.trim(),
        aspectRatio: _aspectRatio,
        outputs: _outputs,
        voiceoverLanguage: null,
      );

      final jobId = await _repo.submitCampaign(request);
      if (mounted) context.push('/generation/$jobId/status');
    } on DioException catch (e) {
      if (!mounted) return;
      final message = e.response?.statusCode == 402
          ? 'Not enough credits.'
          : 'Could not start generation. Please try again.';
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(message)));
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  void dispose() {
    _descriptionCtrl.dispose();
    _industryCtrl.dispose();
    _audienceCtrl.dispose();
    _offerCtrl.dispose();
    _locationCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('New Campaign')),
        body: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const Text('Describe your idea',
                style: TextStyle(fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            TextField(
              controller: _descriptionCtrl,
              maxLines: 5,
              decoration: const InputDecoration(
                hintText:
                    'Small hotel grand opening in Hyderabad. 20% opening week offer. Premium modern campaign.',
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _industryCtrl,
              decoration: const InputDecoration(labelText: 'Industry'),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _locationCtrl,
              decoration: const InputDecoration(labelText: 'Location'),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _audienceCtrl,
              decoration: const InputDecoration(labelText: 'Target audience'),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _offerCtrl,
              decoration: const InputDecoration(labelText: 'Offer / details'),
            ),
            const SizedBox(height: 20),
            Wrap(
              spacing: 8,
              children: AppConstants.styles.map((s) => ChoiceChip(
                    label: Text(s),
                    selected: s == _style,
                    onSelected: (_) => setState(() => _style = s),
                  )).toList(),
            ),
            const SizedBox(height: 20),
            Wrap(
              spacing: 8,
              children: ['4:5', '9:16', '1:1', '16:9'].map((r) => ChoiceChip(
                    label: Text(r),
                    selected: r == _aspectRatio,
                    onSelected: (_) => setState(() => _aspectRatio = r),
                  )).toList(),
            ),
            const SizedBox(height: 20),
            SwitchListTile(
              title: const Text('Premium 4K Poster'),
              value: _outputs.contains(OutputType.poster),
              onChanged: (v) => setState(() =>
                  v ? _outputs.add(OutputType.poster) : _outputs.remove(OutputType.poster)),
            ),
            SwitchListTile(
              title: const Text('Social Video'),
              value: _outputs.contains(OutputType.video),
              onChanged: (v) => setState(() =>
                  v ? _outputs.add(OutputType.video) : _outputs.remove(OutputType.video)),
            ),
            SwitchListTile(
              title: const Text('Caption + Hashtags'),
              value: _outputs.contains(OutputType.caption),
              onChanged: (v) => setState(() =>
                  v ? _outputs.add(OutputType.caption) : _outputs.remove(OutputType.caption)),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitting ? null : _generate,
              child: _submitting
                  ? const CircularProgressIndicator()
                  : const Text('Generate Campaign'),
            ),
          ],
        ),
      );
}
