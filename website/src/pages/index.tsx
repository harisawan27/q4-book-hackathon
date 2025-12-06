import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

// Import SVGs as React components
const NanoBananaPro = require('@site/static/img/nano-banana-pro.svg').default;
const RobotHead = require('@site/static/img/robot-head.svg').default;
const ModuleIcon = require('@site/static/img/module-icon.svg').default;

function ModuleCard({title, description, chapters, link, icon}: {title: string, description: string, chapters: string[], link: string, icon: ReactNode}) {
  return (
    <div className="module-detailed-card">
      <div className="module-card-icon">
        {icon}
      </div>
      <div className="module-card-content">
        <h3>{title}</h3>
        <p>{description}</p>
        <div className="module-chapters">
          <strong>What you'll learn:</strong>
          <ul>
            {chapters.map((chapter, idx) => (
              <li key={idx}>{chapter}</li>
            ))}
          </ul>
        </div>
        <Link className="button button--outline button--primary" to={link}>
          Start {title} →
        </Link>
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="Physical AI & Humanoid Robotics: A Technical Book on Robot Learning">
      
      {/* Hero Section */}
      <header className="home-hero">
        <div className="hero-container container">
          <div className="row">
            <div className="col col--7 hero-text-col">
              <h1 className="hero-title">Physical AI & Humanoid Robotics</h1>
              <p className="hero-subtitle">
                The definitive engineering guide to building autonomous humanoids using ROS 2, Isaac Sim, and Vision-Language-Action Models.
              </p>
              <div className="hero-cta-group">
                <Link
                  className="button-primary-glow"
                  to="/docs/intro">
                  Start Reading
                </Link>
                <Link
                  className="button-github-glow"
                  to="https://github.com/harisawan27/q4-book-hackathon">
                  View on GitHub
                </Link>
              </div>
            </div>
            <div className="col col--5 hero-image-col">
               <div className="hero-robot-container">
                  <RobotHead className="hero-robot-svg" />
               </div>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Introduction / About Section */}
        <section className="intro-section">
           <div className="container">
             <div className="row">
               <div className="col col--8 col--offset-2 text--center">
                 <h2>From Code to Consciousness</h2>
                 <p className="intro-text">
                   Embodied Intelligence is the next frontier of AI. This book bridges the gap between classical control theory and modern deep learning. 
                   You won't just read about robots; you'll build the full software stack for a <strong>Service Humanoid</strong> capable of navigating real-world environments, 
                   manipulating objects, and understanding natural language.
                 </p>
               </div>
             </div>
           </div>
        </section>

        {/* Detailed Curriculum Section */}
        <section className="curriculum-section">
          <div className="container">
            <h2 className="section-title text--center">The Curriculum</h2>
            <div className="modules-list">
              
              <ModuleCard 
                title="Module 1: Robotic Nervous System"
                description="Lay the foundation with the industry-standard middleware for robotics. Understand the graph architecture that powers distributed systems."
                chapters={[
                  "ROS 2 Fundamentals & Architecture",
                  "Nodes, Topics, Services & Actions",
                  "Real-time Control Systems Setup"
                ]}
                link="/docs/module-1/ros2-fundamentals"
                icon={<ModuleIcon className="module-icon-svg" />}
              />

              <ModuleCard 
                title="Module 2: The Digital Twin"
                description="Before breaking hardware, break the simulation. Learn to model physics-accurate robots and environments."
                chapters={[
                  "Unified Robot Description Format (URDF)",
                  "Simulation Environments (Gazebo & Unity)",
                  "Sim-to-Real Transfer Techniques"
                ]}
                link="/docs/module-2/gazebo-unity"
                icon={<ModuleIcon className="module-icon-svg" style={{filter: 'hue-rotate(90deg)'}} />}
              />

              <ModuleCard 
                title="Module 3: AI-Robot Brain"
                description="Equip your robot with eyes and a brain. Implement perception pipelines and train policies using reinforcement learning."
                chapters={[
                  "NVIDIA Isaac Sim & Gym",
                  "Perception Pipelines (YOLO, Depth)",
                  "Deep Reinforcement Learning Training"
                ]}
                link="/docs/module-3/nvidia-isaac"
                icon={<ModuleIcon className="module-icon-svg" style={{filter: 'hue-rotate(180deg)'}} />}
              />

              <ModuleCard 
                title="Module 4: Vision-Language-Action"
                description="The cutting edge. Integrate Large Language Models (LLMs) to enable reasoning, planning, and natural interaction."
                chapters={[
                  "VLA Foundations & Architectures",
                  "Cognitive Planning & Reasoning",
                  "LLM Integration for Command Interpretation"
                ]}
                link="/docs/module-4/vla-foundations"
                icon={<ModuleIcon className="module-icon-svg" style={{filter: 'hue-rotate(270deg)'}} />}
              />

            </div>
          </div>
        </section>

        {/* Capstone Section */}
        <section className="capstone-section">
          <div className="container">
            <h2>The Capstone: Autonomous Service Humanoid</h2>
            <p className="capstone-desc">
              Combine all modules to deploy a complete system. Your final project involves a humanoid robot that can:
            </p>
            <div className="capstone-features row">
               <div className="col col--4">
                 <div className="capstone-feat">🗣️ Understand Voice Commands</div>
               </div>
               <div className="col col--4">
                 <div className="capstone-feat">🧭 Navigate Home Environments</div>
               </div>
               <div className="col col--4">
                 <div className="capstone-feat">🤲 Manipulate Objects safely</div>
               </div>
            </div>
            <div className="capstone-cta">
              <Link
                className="button button--secondary button--lg"
                to="/docs/capstone/project-brief">
                View Project Requirements
              </Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}