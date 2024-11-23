import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <>
      {/* Hero Section */}
      <section className="relative py-20">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-secondary/10 to-background" />
        <div className="container relative">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-foreground">
              AI-Powered Trading on{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                Solana
              </span>
            </h1>
            <p className="mt-6 max-w-2xl mx-auto text-lg sm:text-xl text-muted-foreground">
              Experience the future of automated trading with our advanced AI algorithms
              and seamless Solana integration. Start trading with as little as 0.1 SOL.
            </p>
            <div className="mt-10 flex justify-center gap-4">
              <Link href="/dashboard">
                <Button size="lg" variant="gradient">
                  Launch Dashboard
                </Button>
              </Link>
              <Button size="lg" variant="outline">
                View Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/50">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-lg bg-background shadow-lg">
              <h3 className="text-lg font-semibold mb-2">AI-Powered Strategies</h3>
              <p className="text-muted-foreground">
                Advanced algorithms analyze market patterns and execute trades automatically.
              </p>
            </div>
            <div className="p-6 rounded-lg bg-background shadow-lg">
              <h3 className="text-lg font-semibold mb-2">Real-time Analytics</h3>
              <p className="text-muted-foreground">
                Monitor your portfolio performance with detailed metrics and insights.
              </p>
            </div>
            <div className="p-6 rounded-lg bg-background shadow-lg">
              <h3 className="text-lg font-semibold mb-2">Secure Trading</h3>
              <p className="text-muted-foreground">
                Built on Solana for fast, secure, and low-cost trading operations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trading Metrics Preview */}
      <section className="py-16">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">
            Performance Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="p-6 rounded-lg border bg-card">
              <p className="text-sm text-muted-foreground">Total Value Locked</p>
              <p className="text-2xl font-bold">$2.5M</p>
            </div>
            <div className="p-6 rounded-lg border bg-card">
              <p className="text-sm text-muted-foreground">Active Traders</p>
              <p className="text-2xl font-bold">1,200+</p>
            </div>
            <div className="p-6 rounded-lg border bg-card">
              <p className="text-sm text-muted-foreground">Avg. Monthly Return</p>
              <p className="text-2xl font-bold text-green-500">+8.5%</p>
            </div>
            <div className="p-6 rounded-lg border bg-card">
              <p className="text-sm text-muted-foreground">Total Trades</p>
              <p className="text-2xl font-bold">50K+</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-muted/50">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Start Trading?</h2>
            <p className="text-lg text-muted-foreground mb-8">
              Join thousands of traders using WealthBot to automate their trading
              strategies on Solana.
            </p>
            <Link href="/dashboard">
              <Button size="lg" variant="gradient">
                Get Started Now
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}