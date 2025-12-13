import React from 'react';
import { useNavbarSecondaryMenu } from '@docusaurus/theme-common/internal';
import { NavbarAuth } from '../../components/NavbarAuth';

// This component wraps the default secondary menu to add auth items
function NavbarMobileSidebarSecondaryMenuContent(): JSX.Element | null {
  const secondaryMenu = useNavbarSecondaryMenu();

  return (
    <>
      {/* Render the default secondary menu content */}
      {secondaryMenu.content}

      {/* Add auth items at the bottom */}
      <NavbarAuth mobile />
    </>
  );
}

export default function NavbarMobileSidebarSecondaryMenu(): JSX.Element | null {
  return <NavbarMobileSidebarSecondaryMenuContent />;
}
