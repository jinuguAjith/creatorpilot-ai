import '../domain/auth_repository.dart';

/// MOCK ONLY — used for local UI development and widget tests.
/// Replace with FirebaseAuthRepository in Phase 2. Never ship this
/// implementation to a release build (guarded by Env.isProduction check
/// at DI wiring time, see core/di).
class MockAuthRepository implements AuthRepository {
  final _controller = Stream<AppUser?>.empty();

  @override
  Stream<AppUser?> authStateChanges() => _controller;

  @override
  Future<AppUser> signInWithGoogle() async {
    await Future.delayed(const Duration(milliseconds: 600));
    return const AppUser(
      id: 'mock-user-1',
      email: 'demo@creatorpilot.ai',
      displayName: 'Demo Creator',
    );
  }

  @override
  Future<AppUser> signInWithEmail(String email, String password) async {
    await Future.delayed(const Duration(milliseconds: 600));
    return AppUser(id: 'mock-user-1', email: email, displayName: email.split('@').first);
  }

  @override
  Future<void> signOut() async {}
}
