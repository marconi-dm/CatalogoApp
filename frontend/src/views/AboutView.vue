<script setup lang="ts">
import { onMounted } from 'vue'

interface HistoryItem {
  period: string
  title: string
  text: string
  image: string
}

const history: HistoryItem[] = [
  {
    period: '1871',
    title: 'A fundação da Weir',
    text:
      'George e James Weir fundaram a empresa de engenharia G & J Weir em Glasgow. Os irmãos desenvolveram soluções inovadoras em equipamentos de bombeamento, inicialmente voltadas aos estaleiros do Clyde e aos navios a vapor construídos na região.',
    image:
      'https://res.cloudinary.com/gjkugh3z/image/upload/v1789938542/1871_-_A_funda%C3%A7%C3%A3o_da_Weir.webp',
  },
  {
    period: '1886',
    title: 'Nova oficina de máquinas em Cathcart, Glasgow',
    text:
      'Com o crescimento da empresa, os irmãos estabeleceram uma nova oficina de máquinas e fundição em Cathcart, no sul de Glasgow. A instalação foi construída especialmente para acompanhar a expansão das atividades de engenharia da Weir.',
    image:
      'https://res.cloudinary.com/gjkugh3z/image/upload/v1789938542/1886_-_Nova_oficina_de_m%C3%A1quinas_em_Cathcart_Glasgow.webp',
  },
  {
    period: '1915 — 1950',
    title: 'Ajudando um mundo em mudança',
    text:
      'A Weir ampliou sua atuação para novas áreas da engenharia. Durante a Primeira Guerra Mundial, produziu mais de 1.100 aeronaves e motores. Em 1932, participou do desenvolvimento do autogiro e, em 1946, o Grupo Weir passou a ser listado na Bolsa de Valores de Londres.',
    image:
      'https://res.cloudinary.com/gjkugh3z/image/upload/v1789938543/1915_-_1950_-_Ajudando_um_mundo_em_mudan%C3%A7a.webp',
  },
  {
    period: '1950 — 2010',
    title: 'Crescimento global e aquisições',
    text:
      'Nas décadas seguintes, a Weir expandiu sua presença internacional por meio de aquisições estratégicas. Entre elas, Warman International e SPM fortaleceram significativamente a presença do Grupo nos mercados de mineração, petróleo e gás.',
    image:
      'https://res.cloudinary.com/gjkugh3z/image/upload/v1789938549/1950_-_2010_-_Crescimento_global_e_aquisi%C3%A7%C3%B5es.webp',
  },
  {
    period: '2010 — 2023',
    title: 'Aquisição da ESCO e uma nova fase',
    text:
      'Em 2018, o Grupo Weir realizou sua maior aquisição até então ao incorporar a ESCO por US$ 1,3 bilhão. A operação fortaleceu sua posição em tecnologia para mineração e marcou uma nova etapa na evolução do Grupo.',
    image:
      'https://res.cloudinary.com/gjkugh3z/image/upload/v1789938549/2010_-_2023_-_Aquisi%C3%A7%C3%A3o_da_ESCO_e_celebra%C3%A7%C3%A3o_do_nosso_150%C2%BA_anivers%C3%A1rio.webp',
  },
]

onMounted(() => {
  window.scrollTo({
    top: 0,
    behavior: 'auto',
  })
})
</script>


<template>
  <div class="about-page">

    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="topbar about-topbar">

      <div class="container nav">

        <RouterLink
          to="/"
          class="brand about-brand"
        >
          <img
            class="weir-logo"
            src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789928458/Weir_Group.png"
            alt="Weir Group"
          />

          <span class="brand-line"></span>

          <span class="brand-product">
            ESCO® GET
          </span>
        </RouterLink>


        <div class="nav-right">

          <nav class="navigation">

            <a href="/#catalogo">
              Produtos
            </a>

            <RouterLink
              to="/sobre"
              class="active"
            >
              Sobre
            </RouterLink>

          </nav>


          <div class="quote-contact">

            <a
              class="quote-whatsapp"
              href="https://wa.me/5531987513287?text=Ol%C3%A1%21%20Gostaria%20de%20solicitar%20uma%20cota%C3%A7%C3%A3o%20de%20produtos%20ESCO%20GET."
              target="_blank"
              rel="noopener noreferrer"
            >

              <span class="quote-icon">
                <img
                  src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789932739/wpp_logo.png"
                  alt="WhatsApp"
                />
              </span>

              <span class="quote-text">
                <strong>Cotações</strong>
                <small>(31) 98751-3287</small>
              </span>

            </a>


            <a
              class="quote-email"
              href="mailto:brz-orcamento@mail.weir?subject=Cota%C3%A7%C3%A3o%20ESCO%20GET"
            >
              <span class="quote-text">
                <strong>E-mail</strong>
                <small>brz-orcamento@mail.weir</small>
              </span>
            </a>

          </div>

        </div>

      </div>

    </header>


    <main>

      <!-- =====================================================
           HERO
      ====================================================== -->
      <section class="about-hero">

        <div class="container about-hero-content">

          <span class="about-eyebrow">
            NOSSA HISTÓRIA
          </span>

          <h1>
            Mais de 150 anos
            <span>de engenharia e inovação.</span>
          </h1>

          <p>
            De Glasgow para o mundo. Uma trajetória marcada pela
            evolução da engenharia, pelo desenvolvimento de novas
            tecnologias e pela busca contínua por soluções capazes
            de transformar operações industriais.
          </p>

        </div>

      </section>


      <!-- =====================================================
           HISTORY
      ====================================================== -->
      <section class="history-section">

        <div class="container history-container">

          <article
            v-for="item in history"
            :key="item.period"
            class="history-item"
          >

            <div class="history-image">

              <img
                :src="item.image"
                :alt="`${item.period} - ${item.title}`"
                loading="lazy"
              />

            </div>


            <div class="history-content">

              <span class="history-year">
                {{ item.period }}
              </span>

              <h2>
                {{ item.title }}
              </h2>

              <p>
                {{ item.text }}
              </p>

            </div>

          </article>

        </div>

      </section>


      <!-- =====================================================
           TRANSITION
      ====================================================== -->
      <section class="innovation-transition">

        <div class="container innovation-transition-content">

          <span>
            ENGENHARIA QUE CONTINUA EVOLUINDO
          </span>

          <h2>
            Da história para a tecnologia
            que trabalha no campo.
          </h2>

          <p>
            A mesma cultura de engenharia e inovação que acompanha
            a Weir desde sua fundação continua presente nas soluções
            desenvolvidas para as operações de mineração e construção.
          </p>

        </div>

      </section>


      <!-- =====================================================
           ULTRALOK
      ====================================================== -->
      <section class="ultralok-section">

        <div class="container">

          <div class="ultralok-heading">

            <span class="about-eyebrow">
              ESCO® ULTRALOK®
            </span>

            <div class="ultralok-title-row">

              <h2>
                Simples, mais fácil
                <span>e mais seguro.</span>
              </h2>

              <p>
                Um sistema de dentes de alto desempenho desenvolvido
                para oferecer produtividade, manutenção simplificada
                e maior segurança durante as operações.
              </p>

            </div>

          </div>


          <!-- VIDEO -->
          <div class="ultralok-video-container">

            <video
              class="ultralok-video"
              controls
              playsinline
              preload="metadata"
              poster="https://res.cloudinary.com/gjkugh3z/video/upload/so_29,w_1280,q_auto,f_jpg/ULTRALOK.jpg"
            >
              <source
                src="https://res.cloudinary.com/gjkugh3z/video/upload/v1789868091/ULTRALOK.mp4"
                type="video/mp4"
              />

              Seu navegador não suporta reprodução de vídeo.
            </video>

          </div>


          <!-- SUMMARY -->
          <div class="ultralok-summary">

            <div class="ultralok-overview">

              <span>
                VISÃO GERAL
              </span>

              <h3>
                Mais produtividade.
                Menos manutenção.
              </h3>

              <p>
                O sistema ESCO® Ultralok® utiliza uma trava integrada,
                formando um verdadeiro sistema de duas peças. Isso reduz
                a quantidade de componentes necessários e simplifica
                a substituição das pontas.
              </p>

              <p>
                A instalação e remoção sem marreta contribuem para
                operações mais seguras, enquanto a maior vida útil
                dos dentes ajuda a reduzir intervenções e aumentar
                o tempo disponível da máquina.
              </p>

            </div>


            <div class="ultralok-benefits">

              <article>

                <span class="benefit-number">
                  01
                </span>

                <div>
                  <strong>
                    Trava integrada
                  </strong>

                  <p>
                    Menos componentes para encomendar,
                    armazenar ou perder.
                  </p>
                </div>

              </article>


              <article>

                <span class="benefit-number">
                  02
                </span>

                <div>
                  <strong>
                    Instalação sem marreta
                  </strong>

                  <p>
                    Pontas instaladas e removidas utilizando
                    uma ferramenta de alavanca simples.
                  </p>
                </div>

              </article>


              <article>

                <span class="benefit-number">
                  03
                </span>

                <div>
                  <strong>
                    Menos substituições
                  </strong>

                  <p>
                    Maior vida útil significa menos intervenções
                    durante a operação.
                  </p>
                </div>

              </article>


              <article>

                <span class="benefit-number">
                  04
                </span>

                <div>
                  <strong>
                    Maior disponibilidade
                  </strong>

                  <p>
                    Menos tempo parado para manutenção
                    e mais tempo de máquina trabalhando.
                  </p>
                </div>

              </article>

            </div>

          </div>

        </div>

      </section>


      <!-- =====================================================
           CTA
      ====================================================== -->
      <section class="about-cta">

        <div class="container about-cta-content">

          <div>

            <span>
              ESCO® GROUND ENGAGING TOOLS
            </span>

            <h2>
              Encontre o componente certo
              para sua aplicação.
            </h2>

          </div>


          <a
            href="/#catalogo"
            class="about-cta-button"
          >
            Explorar produtos

            <span>
              →
            </span>
          </a>

        </div>

      </section>

    </main>


    <!-- =====================================================
         FOOTER
    ====================================================== -->
    <footer>

      <div class="container footer-content">

        <div class="footer-brand">

          <img
            class="footer-logo"
            src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789928458/Weir_Group.png"
            alt="Weir Group"
          />

          <span class="footer-brand-line"></span>

          <span class="footer-product">
            ESCO® GET
          </span>

        </div>


        <p>
          Catálogo de produtos
        </p>

      </div>

    </footer>

  </div>
</template>


<style scoped>

/* =====================================================
   PAGE
===================================================== */

.about-page {
  min-height: 100vh;

  color: #27333b;
  background: #ffffff;
}

.about-brand {
  text-decoration: none;
}


/* =====================================================
   HERO
===================================================== */

.about-hero {
  padding: 95px 0 90px;

  border-bottom: 1px solid #edf0f2;

  background: #ffffff;
}

.about-hero-content {
  max-width: 900px;
}

.about-eyebrow {
  display: block;

  margin-bottom: 16px;

  color: #0868c9;

  font-size: 10px;
  font-weight: 700;

  letter-spacing: 2px;
}

.about-hero h1 {
  max-width: 820px;

  margin: 0;

  color: #263139;

  font-size: clamp(48px, 6vw, 76px);
  font-weight: 500;

  line-height: 1;

  letter-spacing: -3.4px;
}

.about-hero h1 span {
  display: block;

  color: #7e878e;

  font-weight: 400;
}

.about-hero p {
  max-width: 650px;

  margin: 28px 0 0;

  color: #727c84;

  font-size: 15px;

  line-height: 1.8;
}


/* =====================================================
   HISTORY
===================================================== */

.history-section {
  padding: 100px 0 130px;
}

.history-container {
  max-width: 1080px;
}

.history-item {
  display: grid;

  grid-template-columns:
    minmax(300px, 0.95fr)
    minmax(320px, 1.05fr);

  align-items: center;

  gap: 62px;

  padding: 55px 0;

  border-bottom: 1px solid #edf0f2;
}

.history-item:first-child {
  padding-top: 0;
}

.history-item:last-child {
  border-bottom: 0;
}


/* =====================================================
   HISTORY IMAGE
===================================================== */

.history-image {
  display: flex;

  align-items: center;
  justify-content: center;

  overflow: hidden;

  width: 100%;

  background: #f3f5f6;
}

.history-image img {
  display: block;

  width: 100%;
  height: auto;

  object-fit: contain;

  transition: transform 0.45s ease;
}

.history-item:hover .history-image img {
  transform: scale(1.015);
}


/* =====================================================
   HISTORY TEXT
===================================================== */

.history-content {
  max-width: 500px;
}

.history-year {
  display: block;

  margin-bottom: 7px;

  color: #0868c9;

  font-size: 11px;
  font-weight: 700;

  letter-spacing: 1.5px;
}

.history-content h2 {
  margin: 0;

  color: #2b343a;

  font-size: clamp(27px, 3vw, 38px);
  font-weight: 500;

  line-height: 1.13;

  letter-spacing: -1.4px;
}

.history-content p {
  margin: 20px 0 0;

  color: #707a82;

  font-size: 14px;

  line-height: 1.75;
}


/* =====================================================
   TRANSITION
===================================================== */

.innovation-transition {
  padding: 105px 0;

  background: #253139;
}

.innovation-transition-content {
  max-width: 780px;
}

.innovation-transition span {
  display: block;

  margin-bottom: 14px;

  color: #78b5ed;

  font-size: 9px;
  font-weight: 700;

  letter-spacing: 1.8px;
}

.innovation-transition h2 {
  margin: 0;

  color: #ffffff;

  font-size: clamp(40px, 5vw, 62px);
  font-weight: 400;

  line-height: 1.04;

  letter-spacing: -2.5px;
}

.innovation-transition p {
  max-width: 620px;

  margin: 27px 0 0;

  color: #bcc4c9;

  font-size: 14px;

  line-height: 1.75;
}


/* =====================================================
   ULTRALOK
===================================================== */

.ultralok-section {
  padding: 115px 0 125px;

  background: #f7f9fa;
}

.ultralok-heading {
  margin-bottom: 50px;
}

.ultralok-title-row {
  display: grid;

  grid-template-columns:
    minmax(0, 1.2fr)
    minmax(300px, 0.8fr);

  align-items: end;

  gap: 80px;
}

.ultralok-title-row h2 {
  margin: 0;

  color: #263139;

  font-size: clamp(42px, 5vw, 65px);
  font-weight: 500;

  line-height: 1;

  letter-spacing: -2.8px;
}

.ultralok-title-row h2 span {
  display: block;

  color: #7b858c;

  font-weight: 400;
}

.ultralok-title-row > p {
  margin: 0;

  color: #707a82;

  font-size: 14px;

  line-height: 1.75;
}


/* =====================================================
   VIDEO
===================================================== */

.ultralok-video-container {
  overflow: hidden;

  width: 100%;

  border-radius: 14px;

  background: #11191e;

  box-shadow:
    0 28px 65px rgba(30, 42, 50, 0.13);
}

.ultralok-video {
  display: block;

  width: 100%;

  max-height: 700px;

  background: #11191e;
}


/* =====================================================
   ULTRALOK SUMMARY
===================================================== */

.ultralok-summary {
  display: grid;

  grid-template-columns:
    minmax(0, 0.9fr)
    minmax(0, 1.1fr);

  gap: 95px;

  padding-top: 68px;
}

.ultralok-overview > span {
  display: block;

  margin-bottom: 12px;

  color: #0868c9;

  font-size: 9px;
  font-weight: 700;

  letter-spacing: 1.7px;
}

.ultralok-overview h3 {
  max-width: 440px;

  margin: 0 0 22px;

  color: #27333b;

  font-size: clamp(31px, 4vw, 46px);
  font-weight: 500;

  line-height: 1.06;

  letter-spacing: -1.8px;
}

.ultralok-overview p {
  max-width: 530px;

  margin: 0 0 15px;

  color: #707b82;

  font-size: 14px;

  line-height: 1.75;
}


/* =====================================================
   BENEFITS
===================================================== */

.ultralok-benefits {
  border-top: 1px solid #dce2e6;
}

.ultralok-benefits article {
  display: grid;

  grid-template-columns: 45px 1fr;

  gap: 20px;

  padding: 22px 0;

  border-bottom: 1px solid #dce2e6;
}

.benefit-number {
  padding-top: 3px;

  color: #0868c9;

  font-size: 9px;
  font-weight: 700;

  letter-spacing: 1px;
}

.ultralok-benefits strong {
  display: block;

  margin-bottom: 5px;

  color: #27333b;

  font-size: 14px;
  font-weight: 600;
}

.ultralok-benefits p {
  margin: 0;

  color: #778189;

  font-size: 12px;

  line-height: 1.6;
}


/* =====================================================
   CTA
===================================================== */

.about-cta {
  padding: 85px 0;

  border-top: 1px solid #e8ecef;

  background: #ffffff;
}

.about-cta-content {
  display: flex;

  align-items: flex-end;
  justify-content: space-between;

  gap: 50px;
}

.about-cta-content > div > span {
  color: #0868c9;

  font-size: 9px;
  font-weight: 700;

  letter-spacing: 1.6px;
}

.about-cta h2 {
  max-width: 630px;

  margin: 11px 0 0;

  color: #27333b;

  font-size: clamp(35px, 4vw, 50px);
  font-weight: 500;

  line-height: 1.05;

  letter-spacing: -2px;
}

.about-cta-button {
  flex-shrink: 0;

  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 22px;

  padding: 14px 18px;

  border: 1px solid #dfe5e8;
  border-radius: 8px;

  color: #27333b;
  background: #ffffff;

  text-decoration: none;

  font-size: 11px;
  font-weight: 600;

  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;
}

.about-cta-button:hover {
  transform: translateY(-2px);

  border-color: #bdcdd8;

  background: #f8fafb;
}


/* =====================================================
   TABLET
===================================================== */

@media (max-width: 950px) {

  .history-item {
    gap: 40px;
  }

  .ultralok-title-row,
  .ultralok-summary {
    grid-template-columns: 1fr;

    gap: 38px;
  }

  .about-cta-content {
    align-items: flex-start;
    flex-direction: column;
  }

}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 650px) {

  .about-hero {
    padding: 65px 0 60px;
  }

  .about-hero h1 {
    font-size: 45px;

    letter-spacing: -2.2px;
  }

  .about-hero p {
    font-size: 14px;
  }


  .history-section {
    padding: 55px 0 80px;
  }

  .history-item {
    display: flex;
    flex-direction: column;

    align-items: stretch;

    gap: 24px;

    padding: 42px 0;
  }

  .history-content {
    max-width: none;
  }

  .history-content h2 {
    font-size: 30px;
  }


  .innovation-transition {
    padding: 70px 0;
  }

  .innovation-transition h2 {
    font-size: 39px;
  }


  .ultralok-section {
    padding: 75px 0 80px;
  }

  .ultralok-heading {
    margin-bottom: 30px;
  }

  .ultralok-title-row h2 {
    font-size: 40px;
  }

  .ultralok-video-container {
    border-radius: 10px;
  }

  .ultralok-summary {
    padding-top: 45px;
  }


  .about-cta {
    padding: 65px 0;
  }

  .about-cta h2 {
    font-size: 35px;
  }

}
</style>