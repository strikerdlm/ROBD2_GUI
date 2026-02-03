/**
 * i18n Configuration for ROBD2 Safety Dashboard
 */

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import translations from './translations';

// Initialize i18next
i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: translations.en },
      es: { translation: translations.es },
    },
    lng: 'es', // Default language (Spanish as per original app)
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false, // React already escapes values
    },
  });

export default i18n;
