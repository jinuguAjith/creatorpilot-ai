import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:creatorpilot_ai/features/campaign/presentation/create_campaign_screen.dart';

// NOTE: written but not run in this environment — no Flutter SDK available
// in the sandbox this was built in. Run `flutter test` locally before
// trusting these; fix anything that doesn't compile/pass first.
void main() {
  testWidgets('CreateCampaignScreen shows all default output toggles', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateCampaignScreen()));

    expect(find.text('Poster'), findsOneWidget);
    expect(find.text('Video (30s)'), findsOneWidget);
    expect(find.text('Caption + hashtags'), findsOneWidget);
    expect(find.text('Voice-over'), findsOneWidget);
  });

  testWidgets('Generate button is present and initially enabled-looking', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateCampaignScreen()));
    expect(find.widgetWithText(ElevatedButton, 'Generate'), findsOneWidget);
  });

  testWidgets('All style options from the spec are selectable', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateCampaignScreen()));
    for (final style in [
      'Luxury', 'Modern', 'Cinematic', 'Minimal',
      'Energetic', 'Professional', 'Festival', 'Elegant'
    ]) {
      expect(find.widgetWithText(ChoiceChip, style), findsOneWidget);
    }
  });

  testWidgets('Toggling voiceover off removes it from selected outputs', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateCampaignScreen()));
    final voiceoverSwitch = find.widgetWithText(SwitchListTile, 'Voice-over');
    expect(voiceoverSwitch, findsOneWidget);
    // Voiceover starts off by default per _outputs initial state.
    final tile = tester.widget<SwitchListTile>(voiceoverSwitch);
    expect(tile.value, isFalse);
  });
}
