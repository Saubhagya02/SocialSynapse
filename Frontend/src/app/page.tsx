// frontend/src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  Sparkles, ArrowRight, Zap, TrendingUp, Calendar,
  BarChart3, Users, Brain, Shield, Globe, Clock
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

export default function Home() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
      // Redirect to dashboard if already logged in
      router.push('/dashboard');
    }
  }, [router]);

  const features = [
    {
      icon: Brain,
      title: "GPT-4 Powered",
      description: "Advanced AI content generation using the latest language models"
    },
    {
      icon: TrendingUp,
      title: "Trend Analysis",
      description: "Stay ahead with real-time industry trend detection"
    },
    {
      icon: Calendar,
      title: "Smart Scheduling",
      description: "Automated posting at optimal engagement times"
    },
    {
      icon: BarChart3,
      title: "Analytics Dashboard",
      description: "Comprehensive insights and performance tracking"
    },
    {
      icon: Users,
      title: "Audience Growth",
      description: "Strategies to expand your professional network"
    },
    {
      icon: Shield,
      title: "Brand Consistency",
      description: "Maintain your unique voice across all content"
    }
  ];

  const stats = [
    { value: "10x", label: "Faster Content Creation" },
    { value: "85%", label: "Engagement Increase" },
    { value: "24/7", label: "Automated Posting" },
    { value: "100+", label: "Content Templates" }
  ];

  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900" />
        
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-purple-300 opacity-20 blur-3xl" />
          <div className="absolute -bottom-40 -left-40 h-80 w-80 rounded-full bg-blue-300 opacity-20 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            {/* Badge */}
            <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur">
              <Sparkles className="mr-2 h-4 w-4 text-yellow-500" />
              <span>Powered by GPT-4 & Advanced AI</span>
            </div>

            {/* Main heading */}
            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
              <span className="block">Transform Your</span>
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                LinkedIn Presence
              </span>
              <span className="block">with AI</span>
            </h1>

            {/* Subheading */}
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
              Generate engaging content, schedule posts automatically, and grow your professional 
              network with our AI-powered LinkedIn automation platform.
            </p>

            {/* CTA Buttons */}
            <div className="mt-10 flex items-center justify-center gap-4">
              <Button
                size="lg"
                onClick={() => router.push('/dashboard')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Learn More
              </Button>
            </div>

            {/* Stats */}
            <div className="mt-16 grid grid-cols-2 gap-8 sm:grid-cols-4">
              {stats.map((stat, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: idx * 0.1 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </div>
                  <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 sm:py-32">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">
              Everything You Need to Succeed on LinkedIn
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
              Powerful features designed to maximize your LinkedIn impact
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="h-full hover:shadow-xl transition-shadow">
                  <CardContent className="p-6">
                    <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-500">
                      <feature.icon className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
                    <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 sm:py-32 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to 10x Your LinkedIn Game?
          </h2>
          <p className="mt-4 text-lg text-blue-100">
            Join thousands of professionals using AI to build their personal brand
          </p>
          <Button
            size="lg"
            variant="secondary"
            onClick={() => router.push('/dashboard')}
            className="mt-8"
          >
            Start Your Free Trial
            <Zap className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
}