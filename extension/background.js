// Background service worker

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'organize') {
    organizeBookmarks().then(result => sendResponse(result));
    return true;
  } else if (request.action === 'removeDuplicates') {
    removeDuplicates().then(result => sendResponse(result));
    return true;
  } else if (request.action === 'checkLinks') {
    checkBrokenLinks().then(result => sendResponse(result));
    return true;
  } else if (request.action === 'report') {
    generateReport().then(result => sendResponse(result));
    return true;
  }
});

async function getAllBookmarks(node, path = '') {
  const bookmarks = [];
  
  if (node.url) {
    bookmarks.push({
      id: node.id,
      title: node.title,
      url: node.url,
      path: path
    });
  }
  
  if (node.children) {
    const newPath = path ? `${path}/${node.title}` : node.title;
    for (const child of node.children) {
      bookmarks.push(...await getAllBookmarks(child, newPath));
    }
  }
  
  return bookmarks;
}

function cleanTitle(title) {
  // Limpiar y formatear título
  title = title.trim();
  
  // Eliminar separadores comunes al final
  title = title.replace(/\s*[|\-–—]\s*$/, '');
  
  // Eliminar espacios múltiples
  title = title.replace(/\s{2,}/g, ' ');
  
  // Eliminar patrones comunes molestos
  title = title.replace(/\s*-\s*(YouTube|Google|Facebook|Twitter|X)$/i, '');
  title = title.replace(/^\[.*?\]\s*/, ''); // Eliminar [tags] al inicio
  
  // Capitalizar apropiadamente si está todo en mayúsculas o minúsculas
  if (title === title.toUpperCase() || title === title.toLowerCase()) {
    // Dividir en palabras y capitalizar cada una
    title = title.toLowerCase().split(' ').map(word => {
      // Palabras que deben quedarse en minúsculas
      const lowercase = ['a', 'an', 'the', 'and', 'or', 'but', 'for', 'at', 'by', 'to', 'de', 'del', 'la', 'el', 'y', 'o', 'en'];
      if (lowercase.includes(word)) return word;
      
      // Palabras técnicas que deben quedarse como están
      const technical = ['html', 'css', 'javascript', 'python', 'java', 'react', 'vue', 'api', 'sql', 'git'];
      if (technical.includes(word)) return word.toUpperCase();
      
      return word.charAt(0).toUpperCase() + word.slice(1);
    }).join(' ');
  }
  
  return title.trim();
}

function categorizeBookmark(bookmark) {
  const title = bookmark.title.toLowerCase();
  const url = bookmark.url.toLowerCase();
  const fullText = title + ' ' + url;
  
  // Educación específica
  if (title.includes('inacap') || url.includes('inacap')) return 'Inacap';
  if (title.includes('tryh4rd') || url.includes('tryh4rd')) return 'TryH4rdCode';
  
  // Trabajo
  if (title.includes('trabajo') || title.includes('work') || url.includes('trabajo')) return 'Trabajo';
  
  // Repositorios de código
  if (url.includes('github.com') || url.includes('gitlab.com') || url.includes('bitbucket.org')) {
    return 'Repositorios';
  }
  
  // Plataformas de aprendizaje
  if (url.includes('udemy.com') || url.includes('coursera.org') || url.includes('platzi.com') ||
      url.includes('edx.org') || url.includes('skillshare.com') || url.includes('domestika.com') ||
      url.includes('learn.microsoft.com') || url.includes('cloud.google.com/learn') ||
      url.includes('freecodecamp.org') || url.includes('codecademy.com') ||
      url.includes('pluralsight.com') || url.includes('linkedin.com/learning')) {
    return 'Cursos Online';
  }
  
  // Documentación oficial
  if ((url.includes('/docs') || url.includes('/documentation') || title.includes('documentation')) &&
      !url.includes('google.com/drive')) {
    return 'Documentacion';
  }
  
  if (url.includes('developer.mozilla.org') || url.includes('w3schools.com') ||
      url.includes('devdocs.io')) {
    return 'Referencias Web';
  }
  
  // Práctica de código
  if (url.includes('leetcode.com') || url.includes('hackerrank.com') || url.includes('codewars.com') ||
      url.includes('exercism.org') || url.includes('codesignal.com') || url.includes('codingame.com') ||
      url.includes('topcoder.com') || url.includes('codeforces.com') ||
      fullText.includes('challenge') || fullText.includes('ejercicio') || fullText.includes('practice')) {
    return 'Ejercicios';
  }
  
  if (url.includes('devchallenges.io') || url.includes('frontendmentor.io') ||
      url.includes('cssbattle.dev')) {
    return 'Desafios Frontend';
  }
  
  // CSS y diseño visual
  if (fullText.includes('css') || fullText.includes('tailwind') || fullText.includes('bootstrap') ||
      fullText.includes('sass') || fullText.includes('styled-components') ||
      url.includes('tailwindcss.com') || url.includes('getbootstrap.com') ||
      url.includes('bulma.io') || url.includes('materializecss.com')) {
    return 'CSS Frameworks';
  }
  
  if (url.includes('coolors.co') || fullText.includes('color') || fullText.includes('palette') ||
      url.includes('paletton.com') || url.includes('colorhunt.co')) {
    return 'Colores';
  }
  
  if (url.includes('fonts.google.com') || fullText.includes('font') || fullText.includes('tipografia') ||
      url.includes('fontsquirrel.com') || url.includes('dafont.com')) {
    return 'Tipografia';
  }
  
  // Diseño y UI
  if (url.includes('dribbble.com') || url.includes('behance.net') || url.includes('awwwards.com') ||
      fullText.includes('inspiration') || fullText.includes('design showcase')) {
    return 'Inspiracion Diseno';
  }
  
  if (url.includes('figma.com') || url.includes('sketch.com') || url.includes('adobe.com/xd') ||
      fullText.includes('wireframe') || fullText.includes('prototype')) {
    return 'Herramientas Diseno';
  }
  
  if (url.includes('uiverse.io') || fullText.includes('component') || fullText.includes('ui kit') ||
      url.includes('uiball.com') || url.includes('loading.io')) {
    return 'Componentes UI';
  }
  
  // HTML y estructura
  if (fullText.includes('html') && !fullText.includes('css')) {
    return 'HTML';
  }
  
  // JavaScript y frameworks
  if (fullText.includes('javascript') || fullText.includes('js') && !fullText.includes('json')) {
    if (fullText.includes('vanilla') || url.includes('javascript.info')) return 'JavaScript Vanilla';
  }
  
  if (fullText.includes('react') || url.includes('react.dev') || url.includes('reactjs.org')) {
    return 'React';
  }
  
  if (fullText.includes('vue') || url.includes('vuejs.org')) return 'Vue';
  if (fullText.includes('angular') || url.includes('angular.io')) return 'Angular';
  if (fullText.includes('svelte') || url.includes('svelte.dev')) return 'Svelte';
  if (fullText.includes('next') || url.includes('nextjs.org')) return 'Next.js';
  if (fullText.includes('typescript') || url.includes('typescriptlang.org')) return 'TypeScript';
  
  // Backend
  if (fullText.includes('node') || fullText.includes('express') || url.includes('nodejs.org') ||
      url.includes('expressjs.com')) {
    return 'Node.js';
  }
  
  if (fullText.includes('python') || url.includes('python.org') || 
      fullText.includes('django') || fullText.includes('flask') || fullText.includes('fastapi')) {
    return 'Python Backend';
  }
  
  if (fullText.includes('php') || fullText.includes('laravel') || fullText.includes('symfony')) {
    return 'PHP';
  }
  
  if (fullText.includes('java') && !fullText.includes('javascript') || fullText.includes('spring')) {
    return 'Java';
  }
  
  if (fullText.includes('api') || fullText.includes('rest') || fullText.includes('graphql') ||
      url.includes('postman.com') || url.includes('insomnia.rest')) {
    return 'APIs';
  }
  
  // Bases de datos
  if (fullText.includes('sql') || fullText.includes('mysql') || fullText.includes('postgres') ||
      fullText.includes('sqlite') || fullText.includes('database')) {
    return 'SQL Databases';
  }
  
  if (fullText.includes('mongodb') || fullText.includes('nosql') || fullText.includes('redis') ||
      fullText.includes('firebase')) {
    return 'NoSQL Databases';
  }
  
  // DevOps y deployment
  if (fullText.includes('docker') || fullText.includes('kubernetes') || fullText.includes('container')) {
    return 'Docker Kubernetes';
  }
  
  if (fullText.includes('aws') || fullText.includes('amazon web services') || url.includes('aws.amazon.com')) {
    return 'AWS';
  }
  
  if (fullText.includes('azure') || url.includes('azure.microsoft.com')) return 'Azure';
  if (fullText.includes('heroku') || url.includes('heroku.com')) return 'Heroku';
  if (fullText.includes('netlify') || url.includes('netlify.com')) return 'Netlify';
  if (fullText.includes('vercel') || url.includes('vercel.com')) return 'Vercel';
  
  if (fullText.includes('deploy') || fullText.includes('hosting') || fullText.includes('cloud')) {
    return 'Hosting Deploy';
  }
  
  // Control de versiones
  if (fullText.includes('git') && !url.includes('github.com') && !url.includes('gitlab.com')) {
    return 'Git';
  }
  
  // Testing
  if (fullText.includes('test') || fullText.includes('jest') || fullText.includes('cypress') ||
      fullText.includes('selenium') || fullText.includes('junit')) {
    return 'Testing';
  }
  
  // Herramientas de desarrollo
  if (url.includes('codepen.io') || url.includes('codesandbox.io') || url.includes('stackblitz.com') ||
      url.includes('replit.com') || url.includes('jsfiddle.net')) {
    return 'Editores Online';
  }
  
  if (fullText.includes('regex') || url.includes('regex101.com') || url.includes('regexr.com')) {
    return 'Regex';
  }
  
  if (fullText.includes('convert') || fullText.includes('transform') || fullText.includes('generator') ||
      url.includes('transform.tools') || url.includes('json') && fullText.includes('format')) {
    return 'Convertidores';
  }
  
  if (fullText.includes('minif') || fullText.includes('compress') || fullText.includes('optimize')) {
    return 'Optimizacion';
  }
  
  // Iconos e imágenes
  if (fullText.includes('icon') || url.includes('fontawesome.com') || url.includes('iconmonstr.com') ||
      url.includes('feathericons.com') || url.includes('heroicons.com')) {
    return 'Iconos';
  }
  
  if (fullText.includes('image') || fullText.includes('photo') || fullText.includes('stock') ||
      url.includes('unsplash.com') || url.includes('pexels.com') || url.includes('pixabay.com')) {
    return 'Imagenes';
  }
  
  // IA y ML
  if (fullText.includes('ai') || fullText.includes('artificial intelligence') || 
      fullText.includes('chatgpt') || fullText.includes('openai') ||
      fullText.includes('machine learning') || fullText.includes('deep learning') ||
      url.includes('huggingface.co') || url.includes('openai.com')) {
    return 'Inteligencia Artificial';
  }
  
  // Contenido multimedia
  if (url.includes('youtube.com') || url.includes('youtu.be')) return 'YouTube';
  if (url.includes('vimeo.com')) return 'Vimeo';
  
  // Blogs y artículos
  if (url.includes('medium.com')) return 'Medium';
  if (url.includes('dev.to')) return 'Dev.to';
  if (url.includes('hashnode.com')) return 'Hashnode';
  
  if (fullText.includes('blog') || fullText.includes('article') || fullText.includes('tutorial')) {
    return 'Blogs Tutoriales';
  }
  
  // Comunidad
  if (url.includes('stackoverflow.com') || url.includes('stackexchange.com')) return 'Stack Overflow';
  if (url.includes('reddit.com')) return 'Reddit';
  if (url.includes('discord.')) return 'Discord';
  
  // Email y comunicación
  if (url.includes('resend.com') || url.includes('sendgrid.com') || fullText.includes('email service')) {
    return 'Email Services';
  }
  
  // Recursos y listas
  if (fullText.includes('awesome') || fullText.includes('resource') || fullText.includes('recurso') ||
      fullText.includes('collection') || fullText.includes('list')) {
    return 'Recursos Colecciones';
  }
  
  // Cheat sheets
  if (fullText.includes('cheat') || fullText.includes('reference') || fullText.includes('quick')) {
    return 'Cheat Sheets';
  }
  
  // Fallback: intenta categorizar por dominio conocido
  const domain = url.split('/')[2];
  if (domain) {
    if (domain.includes('microsoft.com')) return 'Microsoft';
    if (domain.includes('google.com')) return 'Google';
    if (domain.includes('amazon.com')) return 'Amazon';
  }
  
  return 'Sin Categorizar';
}

async function getVisitCount(url) {
  try {
    const visits = await chrome.history.getVisits({url: url});
    return visits ? visits.length : 0;
  } catch (e) {
    return -1; // No se pudo obtener
  }
}

async function organizeBookmarks() {
  try {
    // Obtener todos los bookmarks
    const tree = await chrome.bookmarks.getTree();
    const allBookmarks = [];
    
    for (const root of tree[0].children) {
      allBookmarks.push(...await getAllBookmarks(root));
    }
    
    // PRIMERO: Eliminar duplicados
    const seenUrls = new Set();
    const uniqueBookmarks = [];
    const toRemove = [];
    
    for (const bookmark of allBookmarks) {
      if (seenUrls.has(bookmark.url)) {
        toRemove.push(bookmark.id);
      } else {
        seenUrls.add(bookmark.url);
        uniqueBookmarks.push(bookmark);
      }
    }
    
    // Eliminar duplicados encontrados
    for (const id of toRemove) {
      try {
        await chrome.bookmarks.remove(id);
      } catch (e) {
        // Ignorar si ya fue eliminado
      }
    }
    
    // Obtener conteo de visitas para cada bookmark
    console.log('Obteniendo información de visitas...');
    const bookmarksWithVisits = await Promise.all(
      uniqueBookmarks.map(async (bookmark) => {
        const visitCount = await getVisitCount(bookmark.url);
        return {...bookmark, visitCount};
      })
    );
    
    // Separar en categorías especiales
    const neverVisited = bookmarksWithVisits.filter(b => b.visitCount === 0);
    const mostVisited = bookmarksWithVisits
      .filter(b => b.visitCount > 0)
      .sort((a, b) => b.visitCount - a.visitCount)
      .slice(0, 10);
    
    // Agrupar por categoría (usando solo los únicos, excluyendo los de carpetas especiales)
    const byCategory = {};
    for (const bookmark of bookmarksWithVisits) {
      const category = categorizeBookmark(bookmark);
      if (!byCategory[category]) byCategory[category] = [];
      byCategory[category].push(bookmark);
    }
    
    // Obtener barra de bookmarks
    const bookmarkBar = tree[0].children.find(n => n.id === '1');
    
    // Eliminar todos los hijos actuales
    if (bookmarkBar.children) {
      for (const child of bookmarkBar.children) {
        await chrome.bookmarks.removeTree(child.id);
      }
    }
    
    // 1. Crear carpeta "10 Mas Visitados" al principio
    if (mostVisited.length > 0) {
      const topFolder = await chrome.bookmarks.create({
        parentId: '1',
        title: '⭐ 10 Mas Visitados',
        index: 0
      });
      
      for (const bookmark of mostVisited) {
        await chrome.bookmarks.create({
          parentId: topFolder.id,
          title: `${cleanTitle(bookmark.title)} (${bookmark.visitCount} visitas)`,
          url: bookmark.url
        });
      }
    }
    
    // 2. Crear carpeta "Nunca Visitados"
    if (neverVisited.length > 0) {
      const neverFolder = await chrome.bookmarks.create({
        parentId: '1',
        title: '👻 Nunca Visitados',
        index: 1
      });
      
      for (const bookmark of neverVisited.sort((a, b) => a.title.localeCompare(b.title))) {
        await chrome.bookmarks.create({
          parentId: neverFolder.id,
          title: cleanTitle(bookmark.title),
          url: bookmark.url
        });
      }
    }
    
    // 3. Crear el resto de carpetas por categoría
    for (const [category, bookmarks] of Object.entries(byCategory).sort()) {
      const folder = await chrome.bookmarks.create({
        parentId: '1',
        title: category
      });
      
      // Agregar bookmarks a la carpeta con títulos limpios
      for (const bookmark of bookmarks.sort((a, b) => a.title.localeCompare(b.title))) {
        await chrome.bookmarks.create({
          parentId: folder.id,
          title: cleanTitle(bookmark.title),
          url: bookmark.url
        });
      }
    }
    
    const duplicatesRemoved = toRemove.length;
    return {
      message: `✨ ${uniqueBookmarks.length} bookmarks organizados\n` +
               `📊 ${mostVisited.length} más visitados, ${neverVisited.length} nunca visitados\n` +
               `🧹 ${duplicatesRemoved} duplicados eliminados`
    };
  } catch (error) {
    return {message: error.message};
  }
}

async function removeDuplicates() {
  try {
    const tree = await chrome.bookmarks.getTree();
    const allBookmarks = [];
    
    for (const root of tree[0].children) {
      allBookmarks.push(...await getAllBookmarks(root));
    }
    
    const seen = new Set();
    let removed = 0;
    
    for (const bookmark of allBookmarks) {
      if (seen.has(bookmark.url)) {
        await chrome.bookmarks.remove(bookmark.id);
        removed++;
      } else {
        seen.add(bookmark.url);
      }
    }
    
    return {message: `🧹 ${removed} duplicados eliminados`};
  } catch (error) {
    return {message: error.message};
  }
}

async function checkBrokenLinks() {
  try {
    const tree = await chrome.bookmarks.getTree();
    const allBookmarks = [];
    
    for (const root of tree[0].children) {
      allBookmarks.push(...await getAllBookmarks(root));
    }
    
    const brokenLinks = [];
    const redirects = [];
    let checked = 0;
    
    // Verificar en lotes de 10 para no saturar
    for (let i = 0; i < allBookmarks.length; i += 10) {
      const batch = allBookmarks.slice(i, i + 10);
      
      await Promise.all(batch.map(async (bookmark) => {
        try {
          const response = await fetch(bookmark.url, {
            method: 'HEAD',
            mode: 'no-cors', // Evita problemas de CORS
            cache: 'no-cache'
          });
          
          // En modo no-cors, no podemos ver el status, pero si falla completamente lo sabremos
          checked++;
        } catch (error) {
          brokenLinks.push({
            title: bookmark.title,
            url: bookmark.url,
            error: error.message
          });
        }
      }));
    }
    
    let message = `🔗 Links verificados: ${checked}/${allBookmarks.length}\n`;
    
    if (brokenLinks.length > 0) {
      message += `\n⚠️ ${brokenLinks.length} links con problemas:\n\n`;
      brokenLinks.slice(0, 5).forEach(link => {
        message += `• ${link.title}\n  ${link.url}\n`;
      });
      if (brokenLinks.length > 5) {
        message += `\n... y ${brokenLinks.length - 5} más`;
      }
    } else {
      message += '\n✅ Todos los links parecen estar bien';
    }
    
    return {message, broken: brokenLinks.length};
  } catch (error) {
    return {message: error.message, broken: 0};
  }
}

async function generateReport() {
  try {
    const tree = await chrome.bookmarks.getTree();
    const allBookmarks = [];
    
    for (const root of tree[0].children) {
      allBookmarks.push(...await getAllBookmarks(root));
    }
    
    const byCategory = {};
    for (const bookmark of allBookmarks) {
      const category = categorizeBookmark(bookmark);
      byCategory[category] = (byCategory[category] || 0) + 1;
    }
    
    let report = `📊 Total: ${allBookmarks.length} bookmarks\n\n`;
    for (const [cat, count] of Object.entries(byCategory).sort((a, b) => b[1] - a[1])) {
      report += `${cat}: ${count}\n`;
    }
    
    return {message: report};
  } catch (error) {
    return {message: error.message};
  }
}
