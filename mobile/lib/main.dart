import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'core/routing/app_router.dart';
import 'core/theme/app_theme.dart';
import 'core/constants/app_constants.dart';

// Firebase.initializeApp() is wired in Phase 2 once google-services.json /
// GoogleService-Info.plist are supplied per environment (dev/staging/prod).
// Deliberately NOT called here to avoid a false "it's wired up" impression.
void main() {
  runApp(const ProviderScope(child: CreatorPilotApp()));
}

class CreatorPilotApp extends StatelessWidget {
  const CreatorPilotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.dark,
      routerConfig: appRouter,
    );
  }
}
