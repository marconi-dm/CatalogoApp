<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import type { Product } from './types/Product'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const products = ref<Product[]>([])
const search = ref('')
const selectedType = ref('Todos')

const loading = ref(true)
const error = ref('')

/* PAGINAÇÃO */
const currentPage = ref(1)
const itemsPerPage = 12


function openProduct(id: number) {
  router.push(`/produto/${id}`)
}


async function loadProducts() {
  try {
    loading.value = true
    error.value = ''

    const response = await fetch('/api/products')

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`)
    }

    products.value = await response.json()
  } catch (err) {
    console.error(err)
    error.value = 'Não foi possível carregar os produtos.'
  } finally {
    loading.value = false
  }
}

/* FILTROS */
const filteredProducts = computed(() => {
  const term = search.value.toLowerCase().trim()

  return products.value.filter((product) => {
    const matchesType =
      selectedType.value === 'Todos' ||
      product.item_category === selectedType.value

    const matchesSearch =
      !term ||
      product.pmid?.toLowerCase().includes(term) ||
      product.base_code?.toLowerCase().includes(term) ||
      product.item_description?.toLowerCase().includes(term) ||
      product.specifications?.toLowerCase().includes(term) ||
      product.system_type?.toLowerCase().includes(term) ||
      product.machine?.toLowerCase().includes(term)

    return matchesType && matchesSearch
  })
})

/* TOTAL DE PÁGINAS */
const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage)
})

/* PRODUTOS DA PÁGINA ATUAL */
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage

  return filteredProducts.value.slice(start, end)
})

/* TROCAR PÁGINA */
function goToPage(page: number) {
  if (page < 1 || page > totalPages.value) {
    return
  }

  currentPage.value = page

  document
    .getElementById('catalogo')
    ?.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })
}

/* VOLTA PARA PÁGINA 1 QUANDO PESQUISAR/FILTRAR */
watch([search, selectedType], () => {
  currentPage.value = 1
})

/* IMAGEM CLOUDINARY */
function getProductImage(product: Product) {
  if (!product.media) {
    return ''
  }

  const media = product.media
    .trim()
    .replace(/\s+/g, '_')

  return `https://res.cloudinary.com/gjkugh3z/image/upload/w_700,h_525,c_fit,q_auto,f_auto/${encodeURIComponent(media)}.png`
}

onMounted(() => {
  loadProducts()
})

function getWhatsappLink(product: Product) {
  const whatsappNumber = '5531987513287'

  const pmid = product.pmid?.trim()

  const message = pmid
    ? `Olá! Gostaria de solicitar uma cotação para o produto ESCO GET - PMID ${pmid}.`
    : 'Olá! Gostaria de solicitar uma cotação para este produto ESCO GET.'

  return `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`
}

/* =====================================================
   COMPARTILHAMENTO
===================================================== */

const shareMenuOpen = ref<number | null>(null)

function getShareUrl(product: Product) {
  return `${window.location.origin}/share/produto/${product.id}`
}

async function shareProduct(product: Product) {
  const url = getShareUrl(product)

  const pmid =
    product.pmid?.trim() ||
    'Produto ESCO GET'

  const text =
    `Confira este produto ESCO® GET — PMID ${pmid}.`

  /*
   * MOBILE:
   * usa o compartilhamento nativo do celular
   */
  const isMobile =
    window.matchMedia('(max-width: 650px)').matches

  if (isMobile && navigator.share) {
    try {
      await navigator.share({
        title: `ESCO® GET — PMID ${pmid}`,
        text,
        url,
      })

      return
    } catch (error) {
      if (
        error instanceof Error &&
        error.name === 'AbortError'
      ) {
        return
      }
    }
  }

  /*
   * DESKTOP:
   * abre o menu abaixo do botão
   */
  shareMenuOpen.value =
    shareMenuOpen.value === product.id
      ? null
      : product.id
}


function shareOnWhatsApp(product: Product) {
  const url = getShareUrl(product)

  const pmid =
    product.pmid?.trim() ||
    'Produto ESCO GET'

  const message =
    `Confira este produto ESCO® GET — PMID ${pmid}:\n${url}`

  window.open(
    `https://wa.me/?text=${encodeURIComponent(message)}`,
    '_blank',
    'noopener,noreferrer'
  )

  shareMenuOpen.value = null
}


function shareOnLinkedIn(product: Product) {
  const url = getShareUrl(product)

  window.open(
    `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
    '_blank',
    'noopener,noreferrer'
  )

  shareMenuOpen.value = null
}


async function copyShareLink(product: Product) {
  const url = getShareUrl(product)

  try {
    await navigator.clipboard.writeText(url)
  } catch {
    window.prompt(
      'Copie o link do produto:',
      url
    )
  }

  shareMenuOpen.value = null
}
</script>

<template>
 <RouterView
  v-if="
    route.name === 'product' ||
    route.name === 'about'
  "
/>

  <div
    v-else
    class="site"
  >

    <!-- HEADER -->
    <header class="topbar">
      <div class="container nav">

        <div class="brand">
          <img
            class="weir-logo"
            src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789928458/Weir_Group.png"
            alt="Weir Group"
          />

          <span class="brand-line"></span>

          <span class="brand-product">
            ESCO® GET
          </span>
        </div>


        <div class="nav-right">

          <nav class="navigation">
            <a
              href="#catalogo"
              class="active"
            >
              Produtos
            </a>

            <RouterLink to="/sobre">
              Sobre
            </RouterLink>
          </nav>


          <div class="quote-contact">

            <!-- WHATSAPP -->
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


            <!-- EMAIL -->
            <a
              class="quote-email"
              href="mailto:brz-orcamento@mail.weir?subject=Cota%C3%A7%C3%A3o%20ESCO%20GET"
            >
              <span class="quote-text">
                <strong>
                  E-mail
                </strong>

                <small>
                  brz-orcamento@mail.weir
                </small>
              </span>
            </a>

          </div>

        </div>

      </div>
    </header>


    <!-- VIDEO HERO -->
    <section class="video-hero">

      <video
        class="hero-video"
        autoplay
        muted
        loop
        playsinline
        preload="metadata"
      >
        <source
          src="https://res.cloudinary.com/gjkugh3z/video/upload/so_10,eo_20,w_1280,q_auto:eco,f_auto/ULTRALOK"
        />
      </video>

      <div class="video-overlay"></div>

      <div class="container video-content">

        <div>
          <span class="eyebrow">
            CATÁLOGO DE PRODUTOS
          </span>

          <h1>
            Ground
            <span>Engaging Tools.</span>
          </h1>
        </div>

        <div class="video-description">
          <p>
            Encontre pontas, adaptadores e componentes
            ESCO® para sua aplicação.
          </p>

          <span>
            Consulte por PMID, código ou descrição.
          </span>
        </div>

      </div>

    </section>


    <!-- SEARCH / FILTERS -->
    <section class="tools">

      <div class="container tools-content">

        <div class="search">

          <span class="search-symbol">
            ⌕
          </span>

          <input
            v-model="search"
            type="text"
            placeholder="Pesquisar PMID, código ou produto"
          />

          <button
            v-if="search"
            class="clear"
            @click="search = ''"
          >
            ×
          </button>

        </div>


        <div class="filters">

          <button
            v-for="type in ['Todos', 'POINT', 'ADAPTER']"
            :key="type"
            :class="{ active: selectedType === type }"
            @click="selectedType = type"
          >
            {{
              type === 'POINT'
                ? 'Pontas'
                : type === 'ADAPTER'
                  ? 'Adaptadores'
                  : 'Todos'
            }}
          </button>

        </div>

      </div>

    </section>


    <!-- CATALOG -->
    <main
      id="catalogo"
      class="catalog"
    >

      <div class="container">

        <!-- HEADING -->
        <div class="catalog-heading">

          <h2>
            Produtos
          </h2>

          <span v-if="!loading">
            {{ filteredProducts.length }}
            {{ filteredProducts.length === 1 ? 'item' : 'itens' }}
          </span>

        </div>


        <!-- LOADING -->
        <div
          v-if="loading"
          class="empty"
        >
          <span>
            Carregando produtos...
          </span>
        </div>


        <!-- ERROR -->
        <div
          v-else-if="error"
          class="empty"
        >

          <span>
            {{ error }}
          </span>

          <button @click="loadProducts">
            Tentar novamente
          </button>

        </div>


        <!-- PRODUCTS -->
        <template v-else-if="filteredProducts.length">

          <div class="gallery">

           <article
              v-for="product in paginatedProducts"
              :key="product.id"
              class="product"
              @click="openProduct(product.id)"
            >

              <!-- PRODUCT IMAGE -->
              <div class="image-container">

                <img
                  v-if="product.media"
                  :src="getProductImage(product)"
                  :alt="product.pmid || 'Produto ESCO'"
                  loading="lazy"
                />

                <div
                  v-else
                  class="product-placeholder"
                >
                  <span>
                    ESCO GET
                  </span>
                </div>


                <!-- HOVER -->
                <div class="image-overlay">

                  <span class="view-product">
                    Ver produto
                  </span>

                  <span class="arrow">
                    ↗
                  </span>

                </div>

              </div>


        <!-- PRODUCT INFORMATION -->
        <div class="product-info">

          <div class="product-main-info">

            <span class="pmid">
              PMID
            </span>

            <h3>
              {{ product.pmid || '—' }}
            </h3>

            <p>
              {{
                product.specifications ||
                product.item_description ||
                'Informações técnicas não disponíveis.'
              }}
            </p>

<div class="product-card-footer">

  <span class="product-type">
    {{
      product.item_category === 'POINT'
        ? 'Ponta'
        : product.item_category === 'ADAPTER'
          ? 'Adaptador'
          : product.item_category || 'Produto'
    }}
  </span>


        <div class="product-card-actions">

          <!-- COMPARTILHAR -->
          <div
            class="product-share-wrapper"
            @click.stop
          >

            <button
              type="button"
              class="product-share-button"
              aria-label="Compartilhar produto"
              @click.stop="shareProduct(product)"
            >

              <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  fill="currentColor"
                  d="M18 16a3 3 0 0 0-2.24 1.01L8.91 13.6a3.15 3.15 0 0 0 0-3.2l6.85-3.41A3 3 0 1 0 15 5a2.9 2.9 0 0 0 .09.72L8.24 9.13a3 3 0 1 0 0 5.74l6.85 3.41A2.9 2.9 0 0 0 15 19a3 3 0 1 0 3-3Z"
                />
              </svg>

              <span>
                Compartilhar
              </span>

            </button>


            <!-- MENU DESKTOP -->
            <div
              v-if="shareMenuOpen === product.id"
              class="product-share-menu"
            >

              <button
                type="button"
                @click.stop="shareOnWhatsApp(product)"
              >
                WhatsApp
              </button>

              <button
                type="button"
                @click.stop="shareOnLinkedIn(product)"
              >
                LinkedIn
              </button>

              <button
                type="button"
                @click.stop="copyShareLink(product)"
              >
                Copiar link
              </button>

            </div>

          </div>


          <!-- COTAR -->
          <a
            class="product-quote-button"
            :href="getWhatsappLink(product)"
            target="_blank"
            rel="noopener noreferrer"
            @click.stop
          >

            <img
              src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789932739/wpp_logo.png"
              alt=""
            />

            <span>
              Cotar
            </span>

          </a>

        </div>

      </div>

          </div>

        </div>

            </article>

          </div>


          <!-- PAGINATION -->
          <div
            v-if="totalPages > 1"
            class="pagination"
          >

            <button
              class="pagination-arrow"
              :disabled="currentPage === 1"
              @click="goToPage(currentPage - 1)"
            >
              ←
            </button>


            <button
              v-for="page in totalPages"
              :key="page"
              class="pagination-number"
              :class="{ active: currentPage === page }"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>


            <button
              class="pagination-arrow"
              :disabled="currentPage === totalPages"
              @click="goToPage(currentPage + 1)"
            >
              →
            </button>

          </div>

        </template>


        <!-- EMPTY -->
        <div
          v-else
          class="empty"
        >

          <span>
            Nenhum produto encontrado.
          </span>

          <button
            @click="
              search = '';
              selectedType = 'Todos'
            "
          >
            Limpar pesquisa
          </button>

        </div>

      </div>

    </main>


    <!-- FOOTER -->
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