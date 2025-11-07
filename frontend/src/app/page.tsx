'use client';

import { useTranslation } from "react-i18next";

export default function Home() {

  const { t } = useTranslation('translation', { keyPrefix: 'Landing' });

  return (
    <main className="min-h-screen bg-background centered-display">

      {/* HEADER */}
      <section className="centered-display w-full min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('/landing-background.png')" }}>
        <h1 className="headers">Experiment - 40</h1>
        <h3 className="caption">{t('description')}</h3>
      </section>

      {/* BASIC DESCRIPTION */}
      <section className="px-8 py-20 w-full centered-display flex-col">
        <h3 className="paragraph max-w-4xl">{t('info')}</h3>

        {/* Feature Grid */}
        <div className="w-full max-w-5xl grid grid-cols-1 sm:grid-cols-3 gap-8 mt-16">

          <div className="centered-display flex-col gap-4 p-6 rounded-2xl bg-surface-card/60 border border-text-muted/30 backdrop-blur-sm">
            <img src="https://media.tenor.com/sAertjv-3eMAAAAj/hardcore-heart-minecraft.gif" alt="Hardcore Heart" className="w-16 rounded-lg" loading="lazy" />
            <p className="text-mono text-lg">{t('one_life')}</p>
            <p className="paragraph max-w-xs">{t('feature_one_life_desc')}</p>
          </div>

          <div className="centered-display flex-col gap-4 p-6 rounded-2xl bg-surface-card/60 border border-text-muted/30 backdrop-blur-sm">
            <img src="https://minecraft.wiki/images/Written_Book_JE2_BE2.gif?c6510" alt="Written Book" className="w-16 rounded-lg" loading="lazy" />
            <p className="text-mono text-lg">{t('no_rules')}</p>
            <p className="paragraph max-w-xs">{t('feature_no_rules_desc')}</p>
          </div>

          <div className="centered-display flex-col gap-4 p-6 rounded-2xl bg-surface-card/60 border border-text-muted/30 backdrop-blur-sm">
            <img src="https://minecraft.wiki/images/Enchanted_Iron_Sword.gif?b2d9d" alt="Enchanted Sword" className="w-16 rounded-lg" loading="lazy" />
            <p className="text-mono text-lg">{t('no_safe_zones')}</p>
            <p className="paragraph max-w-xs">{t('feature_no_safe_zones_desc')}</p>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 flex flex-wrap items-center justify-center gap-4">
          <a href="/auth" className="btn btn-primary glow-pulse">{t('cta_join')}</a>
          <a href="/wiki" className="btn btn-outline">{t('cta_learn_more')}</a>
        </div>

        {/* Flavor line */}
        <p className="text-muted mt-8">{t('flavor_line')}</p>
      </section>

    </main>
  );
}
