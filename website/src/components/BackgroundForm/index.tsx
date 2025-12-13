import React from 'react';
import { UserBackground } from '../../lib/auth';

interface BackgroundFormProps {
  value: UserBackground;
  onChange: (background: UserBackground) => void;
  disabled?: boolean;
}

const skillLevels = [
  { value: 'none', label: 'None' },
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
] as const;

const experienceLevels = [
  { value: 'student', label: 'Student' },
  { value: 'professional', label: 'Professional' },
  { value: 'hobbyist', label: 'Hobbyist' },
  { value: 'researcher', label: 'Researcher' },
] as const;

export function BackgroundForm({ value, onChange, disabled = false }: BackgroundFormProps) {
  const handleChange = (field: keyof UserBackground, newValue: string) => {
    onChange({
      ...value,
      [field]: newValue,
    });
  };

  return (
    <div className="background-form">
      <h4>Your Background</h4>
      <p className="text--secondary">
        Help us personalize content to match your experience level.
      </p>

      <div className="margin-bottom--md">
        <label htmlFor="software_skills" className="form-label">
          Software/Programming Skills
        </label>
        <select
          id="software_skills"
          className="form-select"
          value={value.software_skills}
          onChange={(e) => handleChange('software_skills', e.target.value)}
          disabled={disabled}
        >
          {skillLevels.map((level) => (
            <option key={level.value} value={level.value}>
              {level.label}
            </option>
          ))}
        </select>
        <span className="form-helper">
          Experience with Python, ROS 2, or AI/ML
        </span>
      </div>

      <div className="margin-bottom--md">
        <label htmlFor="hardware_skills" className="form-label">
          Hardware/Robotics Skills
        </label>
        <select
          id="hardware_skills"
          className="form-select"
          value={value.hardware_skills}
          onChange={(e) => handleChange('hardware_skills', e.target.value)}
          disabled={disabled}
        >
          {skillLevels.map((level) => (
            <option key={level.value} value={level.value}>
              {level.label}
            </option>
          ))}
        </select>
        <span className="form-helper">
          Experience with robotics, electronics, or mechanical systems
        </span>
      </div>

      <div className="margin-bottom--md">
        <label htmlFor="experience_level" className="form-label">
          Your Role
        </label>
        <select
          id="experience_level"
          className="form-select"
          value={value.experience_level}
          onChange={(e) => handleChange('experience_level', e.target.value)}
          disabled={disabled}
        >
          {experienceLevels.map((level) => (
            <option key={level.value} value={level.value}>
              {level.label}
            </option>
          ))}
        </select>
        <span className="form-helper">
          How would you describe yourself?
        </span>
      </div>
    </div>
  );
}

export default BackgroundForm;
