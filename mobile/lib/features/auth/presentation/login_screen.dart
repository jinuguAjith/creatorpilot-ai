import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_constants.dart';
import '../data/mock_auth_repository.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _repo = MockAuthRepository(); // Phase 2: inject via Riverpod provider
  bool _loading = false;

  Future<void> _signInWithGoogle() async {
    setState(() => _loading = true);
    await _repo.signInWithGoogle();
    if (mounted) context.go('/home');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              Text(AppConstants.appName,
                  style: Theme.of(context)
                      .textTheme
                      .headlineMedium
                      ?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              Text(AppConstants.tagline,
                  style: Theme.of(context).textTheme.bodyLarge),
              const SizedBox(height: 40),
              ElevatedButton.icon(
                onPressed: _loading ? null : _signInWithGoogle,
                icon: const Icon(Icons.g_mobiledata, size: 28),
                label: _loading
                    ? const SizedBox(
                        height: 18,
                        width: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Continue with Google'),
              ),
              const SizedBox(height: 12),
              OutlinedButton(
                onPressed: _loading ? null : () {},
                child: const Text('Continue with Email'),
              ),
              const SizedBox(height: 24),
              const Text(
                'By continuing you agree to our Terms of Service and Privacy Policy.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 12),
              ),
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}
