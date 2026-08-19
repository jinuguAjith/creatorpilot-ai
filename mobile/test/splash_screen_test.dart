import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:creatorpilot_ai/features/splash/presentation/splash_screen.dart';

void main() {
  testWidgets('SplashScreen shows app name and tagline', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: SplashScreen()));
    expect(find.text('CreatorPilot AI'), findsOneWidget);
    expect(find.text('One Idea. Complete Content.'), findsOneWidget);
  });
}
