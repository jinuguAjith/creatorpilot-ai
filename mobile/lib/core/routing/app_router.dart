import 'package:go_router/go_router.dart';

import '../../features/splash/presentation/splash_screen.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/home/presentation/home_screen.dart';
import '../../features/campaign/presentation/create_campaign_screen.dart';
import '../../features/generation/presentation/generation_status_screen.dart';
import '../../features/generation/presentation/generation_result_screen.dart';
import '../../features/projects/presentation/project_history_screen.dart';
import '../../features/brand_kit/presentation/brand_kit_screen.dart';
import '../../features/credits/presentation/credits_screen.dart';

/// Central route table. Auth-gating is handled via `redirect` once
/// `AuthController` is wired to Firebase in Phase 2.
final appRouter = GoRouter(
  initialLocation: '/splash',
  routes: [
    GoRoute(path: '/splash', builder: (c, s) => const SplashScreen()),
    GoRoute(path: '/login', builder: (c, s) => const LoginScreen()),
    GoRoute(path: '/home', builder: (c, s) => const HomeScreen()),
    GoRoute(
      path: '/campaign/new',
      builder: (c, s) => const CreateCampaignScreen(),
    ),
    GoRoute(
      path: '/generation/:jobId/status',
      builder: (c, s) => GenerationStatusScreen(jobId: s.pathParameters['jobId']!),
    ),
    GoRoute(
      path: '/generation/:jobId/result',
      builder: (c, s) => GenerationResultScreen(jobId: s.pathParameters['jobId']!),
    ),
    GoRoute(path: '/projects', builder: (c, s) => const ProjectHistoryScreen()),
    GoRoute(path: '/brand-kit', builder: (c, s) => const BrandKitScreen()),
    GoRoute(path: '/credits', builder: (c, s) => const CreditsScreen()),
  ],
);
