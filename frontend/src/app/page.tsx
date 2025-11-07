'use client';

import { useTranslation } from "react-i18next";

export default function Home() {

  const { t } = useTranslation('translation', { keyPrefix: 'Landing' });

  return (
    <main className="min-h-screen bg-background centered-display">

      {/* Header Section */}
      <section
        className="centered-display w-full min-h-screen bg-cover bg-center"
        style={{ backgroundImage: "url('/landing-background.png')" }}
      >
        <h1 className="headers">Experiment - 40</h1>
        <h3 className="caption">{t('description')}</h3>
      </section>

      {/* Basic Description */}
      <section className="px-8 py-16 w-full centered-display min-h-screen">
        <h3 className="paragraph">{t('info')}</h3>

        <div className="w-full max-w-3xl grid md:grid-cols-3 lg:grid-cols-3 grid-cols-1 gap-16 mt-16">

          <div className="centered-display gap-4">
            <img src='https://minecraft.wiki/images/Written_Book_JE2_BE2.gif?c6510' className="w-16" />
            <p className="text-mono">{t('no_rules')}</p>
          </div>

          <div className="centered-display gap-4">
            <img src='https://media.tenor.com/sAertjv-3eMAAAAj/hardcore-heart-minecraft.gif' className="w-16" />
            <p className="text-mono">{t('one_life')}</p>
          </div>

          <div className="centered-display gap-4">
            <img src='https://minecraft.wiki/images/Enchanted_Iron_Sword.gif?b2d9d' className="w-16" />
            <p className="text-mono">{t('no_safe_zones')}</p>
          </div>
        </div>
      </section>

    </main>
  );
}
