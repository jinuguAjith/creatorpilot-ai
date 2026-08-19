import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:creatorpilot_ai/features/home/presentation/home_screen.dart';

// NOTE: written but not run in this environment — no Flutter SDK available
// in the sandbox this was built in. Run `flutter test` locally before
// trusting these.
void main() {
  Widget wrapWithRouter(Widget child) {
    final router = GoRouter(routes: [
      GoRoute(path: '/', builder: (c, s) => child),
      GoRoute(path: '/campaign/new', builder: (c, s) => const Scaffold(body: Text('Campaign screen'))),
      GoRoute(path: '/projects', builder: (c, s) => const Scaffold(body: Text('Projects screen'))),
      GoRoute(path: '/brand-kit', builder: (c, s) => const Scaffold(body: Text('Brand kit screen'))),
      GoRoute(path: '/credits', builder: (c, s) => const Scaffold(body: Text('Credits screen'))),
    ]);
    return MaterialApp.router(routerConfig: router);
  }

  testWidgets('HomeScreen shows Create New Campaign CTA', (tester) async {
    await tester.pumpWidget(wrapWithRouter(const HomeScreen()));
    expect(find.text('Create New Campaign'), findsOneWidget);
  });

  testWidgets('Tapping Create New Campaign navigates to campaign screen', (tester) async {
    await tester.pumpWidget(wrapWithRouter(const HomeScreen()));
    await tester.tap(find.text('Create New Campaign'));
    await tester.pumpAndSettle();
    expect(find.text('Campaign screen'), findsOneWidget);
  });

  testWidgets('HomeScreen shows Brand Kit quick link', (tester) async {
    await tester.pumpWidget(wrapWithRouter(const HomeScreen()));
    expect(find.text('Brand Kit'), findsOneWidget);
  });
}
