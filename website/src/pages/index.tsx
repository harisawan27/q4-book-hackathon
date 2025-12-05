import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="Physical AI & Humanoid Robotics: A Technical Book on Robot Learning">
      
      {/* Hero Section */}
      <header className="home-hero">
        <div className="hero-content">
          <h1 className="hero-title">Physical AI & Humanoid Robotics</h1>
          <p className="hero-subtitle">
            A comprehensive engineering guide to ROS 2, Isaac Sim, and Vision-Language-Action Models.
          </p>
          <div className="hero-cta">
            <Link
              className="button-primary-glow"
              to="/docs/intro">
              Start Reading
            </Link>
          </div>
        </div>
      </header>

      <main>
        {/* Features Grid */}
        <section className="features-section">
          <div className="features-grid">
            
            <div className="feature-card">
              <span className="feature-icon">🧠</span>
              <h3>Module 1: The Nervous System</h3>
              <p>
                Master <strong>ROS 2 Humble</strong>. Learn nodes, topics, services, and how to architect real-time control systems for complex robots.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">🌐</span>
              <h3>Module 2: The Digital Twin</h3>
              <p>
                Build physics-accurate simulations. From <strong>URDF</strong> modeling to high-fidelity environments in <strong>NVIDIA Isaac Sim</strong>.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">👁️</span>
              <h3>Module 3: Perception & RL</h3>
              <p>
                Train robots using <strong>Reinforcement Learning</strong> (Isaac Gym) and build robust perception pipelines with YOLO and Depth fusion.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">🤖</span>
              <h3>Module 4: Cognitive Planning</h3>
              <p>
                Integrate <strong>Large Language Models (LLMs)</strong> and VLA models to give your robot common sense and high-level reasoning capabilities.
              </p>
            </div>

          </div>
        </section>

        {/* Capstone Section */}
        <section className="capstone-section">
          <div className="container">
            <h2>The Capstone Project</h2>
            <p>
              Apply everything you've learned to build a fully autonomous <strong>Service Humanoid</strong> capable of understanding natural language commands and manipulating objects in a home environment.
            </p>
            <Link
              className="button button--secondary button--lg"
              to="/docs/capstone/project-brief">
              View Project Brief
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}