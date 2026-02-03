/**
 * Main Layout Component
 * 
 * Provides the application shell with sidebar navigation
 * and responsive layout for the safety dashboard.
 */

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Plug,
  Stethoscope,
  Target,
  Calculator,
  FileCode,
  FileText,
  Activity,
  Menu,
  X,
  Globe,
  ChevronRight,
} from 'lucide-react';
import type { PageKey } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  currentPage: PageKey;
  onNavigate: (page: PageKey) => void;
  isConnected: boolean;
}

const navItems: { key: PageKey; icon: React.ReactNode }[] = [
  { key: 'dashboard', icon: <LayoutDashboard size={20} /> },
  { key: 'connection', icon: <Plug size={20} /> },
  { key: 'diagnostics', icon: <Stethoscope size={20} /> },
  { key: 'calibration', icon: <Target size={20} /> },
  { key: 'gasCalculators', icon: <Calculator size={20} /> },
  { key: 'programs', icon: <FileCode size={20} /> },
  { key: 'logging', icon: <FileText size={20} /> },
  { key: 'performance', icon: <Activity size={20} /> },
];

export function Layout({ children, currentPage, onNavigate, isConnected }: LayoutProps) {
  const { t, i18n } = useTranslation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'es' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <div className="min-h-screen flex">
      {/* Desktop Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: sidebarOpen ? 280 : 80 }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="hidden lg:flex flex-col glass-card rounded-none border-r border-white/10 fixed left-0 top-0 bottom-0 z-40"
      >
        {/* Logo */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-primary-500/30">
              <Activity size={24} className="text-white" />
            </div>
            <AnimatePresence>
              {sidebarOpen && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  <h1 className="text-xl font-bold text-white">ROBD2</h1>
                  <p className="text-xs text-gray-400 truncate">Safety Dashboard</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Connection Status */}
        <div className="px-4 py-3 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 shadow-lg shadow-green-500/50 animate-pulse' : 'bg-red-500 shadow-lg shadow-red-500/50'}`} />
            <AnimatePresence>
              {sidebarOpen && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className={`text-sm font-medium ${isConnected ? 'text-green-400' : 'text-red-400'}`}
                >
                  {isConnected ? t('connection.connected') : t('connection.disconnected')}
                </motion.span>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-thin">
          {navItems.map((item) => (
            <button
              key={item.key}
              onClick={() => onNavigate(item.key)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                currentPage === item.key
                  ? 'bg-gradient-to-r from-primary-600/30 to-primary-500/20 text-white border-l-2 border-primary-500'
                  : 'text-gray-400 hover:bg-white/10 hover:text-white'
              }`}
            >
              {item.icon}
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                    className="font-medium"
                  >
                    {t(`nav.${item.key}`)}
                  </motion.span>
                )}
              </AnimatePresence>
              {currentPage === item.key && sidebarOpen && (
                <ChevronRight size={16} className="ml-auto text-primary-400" />
              )}
            </button>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-white/10 space-y-3">
          {/* Language Toggle */}
          <button
            onClick={toggleLanguage}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:bg-white/10 hover:text-white transition-all duration-200"
          >
            <Globe size={20} />
            <AnimatePresence>
              {sidebarOpen && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="font-medium"
                >
                  {i18n.language === 'en' ? 'Español' : 'English'}
                </motion.span>
              )}
            </AnimatePresence>
          </button>

          {/* Collapse Button */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:bg-white/10 hover:text-white transition-all duration-200"
          >
            <motion.div
              animate={{ rotate: sidebarOpen ? 0 : 180 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronRight size={20} />
            </motion.div>
          </button>
        </div>
      </motion.aside>

      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 glass-card rounded-none border-b border-white/10">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center">
              <Activity size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">ROBD2</h1>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-xs text-gray-400">
                  {isConnected ? t('connection.connected') : t('connection.disconnected')}
                </span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-xl text-gray-400 hover:bg-white/10 hover:text-white"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="lg:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
            onClick={() => setMobileMenuOpen(false)}
          >
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="w-80 h-full glass-card rounded-none"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6 border-b border-white/10">
                <h2 className="text-lg font-bold text-white">{t('appTitle')}</h2>
              </div>
              <nav className="p-4 space-y-2">
                {navItems.map((item) => (
                  <button
                    key={item.key}
                    onClick={() => {
                      onNavigate(item.key);
                      setMobileMenuOpen(false);
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                      currentPage === item.key
                        ? 'bg-primary-600/30 text-white'
                        : 'text-gray-400 hover:bg-white/10 hover:text-white'
                    }`}
                  >
                    {item.icon}
                    <span className="font-medium">{t(`nav.${item.key}`)}</span>
                  </button>
                ))}
              </nav>
              <div className="p-4 border-t border-white/10">
                <button
                  onClick={toggleLanguage}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:bg-white/10 hover:text-white"
                >
                  <Globe size={20} />
                  <span className="font-medium">
                    {i18n.language === 'en' ? 'Español' : 'English'}
                  </span>
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main
        className={`flex-1 transition-all duration-300 ${
          sidebarOpen ? 'lg:ml-[280px]' : 'lg:ml-20'
        } pt-20 lg:pt-0`}
      >
        <div className="p-6 lg:p-8 min-h-screen">
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {children}
          </motion.div>
        </div>
      </main>
    </div>
  );
}

export default Layout;
