<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Product } from '../types/Product'

interface CompatibleProducts {
  adapters: Product[]
  points: Product[]
  locks: Product[]
  pin_collar: Product[]
}

interface ProductDetails extends Product {
  compatible: CompatibleProducts
}

interface Dimensions {
  A?: string
  B?: string
  C?: string
  D?: string
}

const route = useRoute()
const router = useRouter()

const product = ref<ProductDetails | null>(null)
const loading = ref(true)
const error = ref('')


/* =========================================================
   MENSAGEM WHATSAPP
========================================================= */

const whatsappNumber = '5531987513287'

const whatsappLink = computed(() => {
  const pmid = product.value?.pmid?.trim()

  const message = pmid
    ? `Olá! Gostaria de solicitar uma cotação para o produto ESCO GET - PMID ${pmid}.`
    : 'Olá! Gostaria de solicitar uma cotação de produtos ESCO GET.'

  return `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`
})


const productId = computed(() => Number(route.params.id))

const specificationImage =
  'https://res.cloudinary.com/gjkugh3z/image/upload/v1789874481/ESPEC.png'


/* =========================================================
   CARREGAR PRODUTO
========================================================= */

async function loadProduct() {
  try {
    loading.value = true
    error.value = ''

    const response = await fetch(`/api/products/${productId.value}`)

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`)
    }

    product.value = await response.json()
  } catch (err) {
    console.error(err)
    error.value = 'Não foi possível carregar o produto.'
  } finally {
    loading.value = false
  }
}


/* =========================================================
   IMAGENS CLOUDINARY
========================================================= */

function getProductImage(item: Product) {
  if (!item.media) {
    return ''
  }

  const media = item.media
    .trim()
    .replace(/\s+/g, '_')

  return `https://res.cloudinary.com/gjkugh3z/image/upload/w_900,h_700,c_fit,q_auto,f_auto/${encodeURIComponent(media)}.png`
}


/* =========================================================
   DESCRIÇÃO SEM AS MEDIDAS
========================================================= */

const cleanDescription = computed(() => {
  if (!product.value) {
    return ''
  }

  const text =
    product.value.specifications ||
    product.value.item_description ||
    ''

  return text
    .replace(/Medidas\s*:\s*.*$/i, '')
    .trim()
})


/* =========================================================
   EXTRAIR MEDIDAS A / B / C / D
========================================================= */

const dimensions = computed<Dimensions | null>(() => {
  const text = product.value?.specifications

  if (!text) {
    return null
  }

  const medidasIndex = text.search(/Medidas\s*:/i)

  if (medidasIndex === -1) {
    return null
  }

  const medidasText = text.slice(medidasIndex)

  const result: Dimensions = {}

  const matches = medidasText.matchAll(
    /\b([ABCD])\s*:\s*([\d.,]+)/gi
  )

for (const match of matches) {
  const dimensionKey = match[1]
  const dimensionValue = match[2]

  if (!dimensionKey || !dimensionValue) {
    continue
  }

  const key = dimensionKey.toUpperCase() as keyof Dimensions

  result[key] = dimensionValue
}

  return Object.keys(result).length
    ? result
    : null
})


/* =========================================================
   FORMATAR PESO
========================================================= */

function formatWeight(weight: number | null) {
  if (weight === null) {
    return '—'
  }

  return `${weight.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} kg`
}


/* =========================================================
   NOME DA CATEGORIA
========================================================= */

function categoryName(category: string | null) {
  switch (category) {
    case 'POINT':
      return 'PONTA'

    case 'MAXDRP POINT':
      return 'PONTA MAXDRP'

    case 'ADAPTER':
      return 'ADAPTADOR'

    case 'LOCK':
      return 'LOCK'

    case 'PIN/COLLAR':
      return 'PIN / COLLAR'

    default:
      return category || 'PRODUTO'
  }
}


/* =========================================================
   NAVEGAÇÃO
========================================================= */

function goBack() {
  router.push('/')
}

function openProduct(id: number) {
  router.push(`/produto/${id}`)
}


/* =========================================================
   ALTERAÇÃO DE PRODUTO
========================================================= */

watch(
  () => route.params.id,
  () => {
    loadProduct()

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  },
)

onMounted(() => {
  loadProduct()
})
</script>


<template>
  <div class="product-page">

    <!-- HEADER -->
    <header class="detail-header">

      <div class="detail-container detail-nav">

        <button
          class="back-button"
          @click="goBack"
        >
          ← Voltar aos produtos
        </button>

        <div class="detail-brand">

            <img
                class="detail-logo"
                src="https://res.cloudinary.com/gjkugh3z/image/upload/v1789928458/Weir_Group.png"
                alt="Weir Group"
            />

            <span class="detail-brand-line"></span>

            <small>
                ESCO® GET
            </small>

        </div>

      </div>

    </header>


    <!-- LOADING -->
    <div
      v-if="loading"
      class="detail-state"
    >
      Carregando produto...
    </div>


    <!-- ERROR -->
    <div
      v-else-if="error"
      class="detail-state"
    >
      {{ error }}
    </div>


    <!-- PRODUCT -->
    <main
      v-else-if="product"
      class="product-detail"
    >

      <div class="detail-container">


        <!-- =================================================
             PRODUTO PRINCIPAL
        ================================================== -->

        <section class="product-hero">


          <!-- IMAGE -->
          <div class="detail-image">

            <img
              v-if="product.media"
              :src="getProductImage(product)"
              :alt="product.pmid || 'Produto ESCO'"
            />

            <div
              v-else
              class="detail-placeholder"
            >
              ESCO GET
            </div>

          </div>


          <!-- INFORMATION -->
          <div class="detail-info">

            <span class="detail-category">
              {{ categoryName(product.item_category) }}
            </span>

            <h1>
              {{ product.pmid || '—' }}
            </h1>

            <p class="detail-description">
              {{
                cleanDescription ||
                'Informações técnicas não disponíveis.'
              }}
            </p>


            <!-- TECHNICAL INFO -->
            <div class="detail-specs">

              <div>

                <span>
                  Sistema
                </span>

                <strong>
                  {{ product.system_type || '—' }}
                </strong>

              </div>


              <div>

                <span>
                  Aplicação
                </span>

                <strong>
                  {{ product.machine || '—' }}
                </strong>

              </div>


              <div>

                <span>
                  Base
                </span>

                <strong>
                  {{ product.base_code || '—' }}
                </strong>

              </div>


              <div>

                <span>
                  Peso
                </span>

                <strong>
                  {{ formatWeight(product.unit_weight) }}
                </strong>

              </div>

            </div>

          </div>

        </section>



        <!-- =================================================
             DIMENSÕES
        ================================================== -->

        <section
          v-if="dimensions"
          class="dimensions-section"
        >

          <div class="section-heading">

            <span>
              ESPECIFICAÇÕES TÉCNICAS
            </span>

            <h2>
              Dimensões
            </h2>

            <p>
              Consulte o desenho técnico para identificar
              cada ponto de medição.
            </p>

          </div>


          <div class="dimensions-content">


            <!-- TECHNICAL DRAWING -->
            <div class="dimensions-image">

              <img
                :src="specificationImage"
                alt="Referência das dimensões A, B, C e D"
              />

            </div>


            <!-- VALUES -->
            <div class="dimensions-values">

              <div
                v-if="dimensions.A"
                class="dimension-card"
              >

                <span class="dimension-letter">
                  A
                </span>

                <div>

                  <small>
                    Dimensão A
                  </small>

                  <strong>
                    {{ dimensions.A }}
                    <span>mm</span>
                  </strong>

                </div>

              </div>


              <div
                v-if="dimensions.B"
                class="dimension-card"
              >

                <span class="dimension-letter">
                  B
                </span>

                <div>

                  <small>
                    Dimensão B
                  </small>

                  <strong>
                    {{ dimensions.B }}
                    <span>mm</span>
                  </strong>

                </div>

              </div>


              <div
                v-if="dimensions.C"
                class="dimension-card"
              >

                <span class="dimension-letter">
                  C
                </span>

                <div>

                  <small>
                    Dimensão C
                  </small>

                  <strong>
                    {{ dimensions.C }}
                    <span>mm</span>
                  </strong>

                </div>

              </div>


              <div
                v-if="dimensions.D"
                class="dimension-card"
              >

                <span class="dimension-letter">
                  D
                </span>

                <div>

                  <small>
                    Dimensão D
                  </small>

                  <strong>
                    {{ dimensions.D }}
                    <span>mm</span>
                  </strong>

                </div>

              </div>

            </div>

          </div>

        </section>



        <!-- =================================================
             ADAPTADORES
        ================================================== -->

        <section
          v-if="product.compatible.adapters.length"
          class="compatible-section"
        >

          <div class="compatible-heading">

            <div>

              <span>
                COMPATIBILIDADE
              </span>

              <h2>
                Adaptadores compatíveis
              </h2>

            </div>


            <span class="compatible-count">

              {{ product.compatible.adapters.length }}

              {{
                product.compatible.adapters.length === 1
                  ? 'adaptador'
                  : 'adaptadores'
              }}

            </span>

          </div>


          <div class="compatible-grid">

            <article
              v-for="item in product.compatible.adapters"
              :key="item.id"
              class="compatible-card"
              @click="openProduct(item.id)"
            >

              <div class="compatible-image">

                <img
                  v-if="item.media"
                  :src="getProductImage(item)"
                  :alt="item.pmid || 'Adaptador ESCO'"
                  loading="lazy"
                />

                <div
                  v-else
                  class="detail-placeholder"
                >
                  ESCO GET
                </div>

              </div>


              <div class="compatible-info">

                <span>
                  ADAPTADOR
                </span>

                <h3>
                  {{ item.pmid }}
                </h3>

                <p>
                  {{
                    item.specifications ||
                    item.item_description
                  }}
                </p>

                <small>
                  {{ formatWeight(item.unit_weight) }}
                </small>

              </div>

            </article>

          </div>

        </section>



        <!-- =================================================
             LOCKS
        ================================================== -->

        <section
          v-if="product.compatible.locks.length"
          class="compatible-section"
        >

          <div class="compatible-heading">

            <div>

              <span>
                SISTEMA DE RETENÇÃO
              </span>

              <h2>
                Travas compatíveis
              </h2>

            </div>

          </div>


          <div class="compatible-grid">

            <article
              v-for="item in product.compatible.locks"
              :key="item.id"
              class="compatible-card"
              @click="openProduct(item.id)"
            >

              <div class="compatible-image">

                <img
                  v-if="item.media"
                  :src="getProductImage(item)"
                  :alt="item.pmid || 'Lock ESCO'"
                  loading="lazy"
                />

                <div
                  v-else
                  class="detail-placeholder"
                >
                  ESCO GET
                </div>

              </div>


              <div class="compatible-info">

                <span>
                  LOCK
                </span>

                <h3>
                  {{ item.pmid }}
                </h3>

                <p>
                  {{
                    item.specifications ||
                    item.item_description
                  }}
                </p>

              </div>

            </article>

          </div>

        </section>



        <!-- =================================================
             PIN / COLLAR
        ================================================== -->

        <section
          v-if="product.compatible.pin_collar.length"
          class="compatible-section"
        >

          <div class="compatible-heading">

            <div>

              <span>
                SISTEMA DE RETENÇÃO
              </span>

              <h2>
                Pin / Collar compatíveis
              </h2>

            </div>

          </div>


          <div class="compatible-grid">

            <article
              v-for="item in product.compatible.pin_collar"
              :key="item.id"
              class="compatible-card"
              @click="openProduct(item.id)"
            >

              <div class="compatible-image">

                <img
                  v-if="item.media"
                  :src="getProductImage(item)"
                  :alt="item.pmid || 'Pin Collar ESCO'"
                  loading="lazy"
                />

                <div
                  v-else
                  class="detail-placeholder"
                >
                  ESCO GET
                </div>

              </div>


              <div class="compatible-info">

                <span>
                  PIN / COLLAR
                </span>

                <h3>
                  {{ item.pmid }}
                </h3>

                <p>
                  {{
                    item.specifications ||
                    item.item_description
                  }}
                </p>

              </div>

            </article>

          </div>

        </section>



        <!-- =================================================
             PONTAS
        ================================================== -->

        <section
          v-if="product.compatible.points.length"
          class="compatible-section"
        >

          <div class="compatible-heading">

            <div>

              <span>
                COMPATIBILIDADE
              </span>

              <h2>
                Pontas compatíveis
              </h2>

            </div>

          </div>


          <div class="compatible-grid">

            <article
              v-for="item in product.compatible.points"
              :key="item.id"
              class="compatible-card"
              @click="openProduct(item.id)"
            >

              <div class="compatible-image">

                <img
                  v-if="item.media"
                  :src="getProductImage(item)"
                  :alt="item.pmid || 'Ponta ESCO'"
                  loading="lazy"
                />

                <div
                  v-else
                  class="detail-placeholder"
                >
                  ESCO GET
                </div>

              </div>


              <div class="compatible-info">

                <span>
                  {{ categoryName(item.item_category) }}
                </span>

                <h3>
                  {{ item.pmid }}
                </h3>

                <p>
                  {{
                    item.specifications ||
                    item.item_description
                  }}
                </p>

                <small>
                  {{ formatWeight(item.unit_weight) }}
                </small>

              </div>

            </article>

          </div>

        </section>

      </div>

    </main>

  </div>
</template>