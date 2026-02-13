"""Skill for categorizing bookmarks based on content."""

from typing import Dict, List, Optional
from ..domain.models import Bookmark


class CategorizationSkill:
    """Provee capacidades de clasificación inteligente para bookmarks."""

    def categorize(self, bookmark: Bookmark) -> str:
        """
        Determina la mejor categoría para un bookmark.
        Ported from extension/background.js
        """
        title = (bookmark.title or "").lower()
        url = (bookmark.url or "").lower()
        full_text = f"{title} {url}"

        # Educación específica
        if "inacap" in title or "inacap" in url:
            return "Inacap"
        if "tryh4rd" in title or "tryh4rd" in url:
            return "TryH4rdCode"

        # Trabajo
        if "trabajo" in title or "work" in title or "trabajo" in url:
            return "Trabajo"

        # Repositorios de código
        if any(d in url for d in ["github.com", "gitlab.com", "bitbucket.org"]):
            return "Repositorios"

        # Plataformas de aprendizaje
        if any(
            d in url
            for d in [
                "udemy.com",
                "coursera.org",
                "platzi.com",
                "edx.org",
                "skillshare.com",
                "domestika.com",
                "learn.microsoft.com",
                "cloud.google.com/learn",
                "freecodecamp.org",
                "codecademy.com",
                "pluralsight.com",
                "linkedin.com/learning",
            ]
        ):
            return "Cursos Online"



        # Práctica de código
        if any(
            d in url
            for d in [
                "leetcode.com",
                "hackerrank.com",
                "codewars.com",
                "exercism.org",
                "codesignal.com",
                "codingame.com",
                "topcoder.com",
                "codeforces.com",
            ]
        ) or any(k in full_text for k in ["challenge", "ejercicio", "practice"]):
            return "Ejercicios"

        if any(
            d in url
            for d in ["devchallenges.io", "frontendmentor.io", "cssbattle.dev"]
        ):
            return "Desafios Frontend"

        # CSS y diseño visual
        if any(
            k in full_text
            for k in ["css", "tailwind", "bootstrap", "sass", "styled-components"]
        ) or any(
            d in url
            for d in [
                "tailwindcss.com",
                "getbootstrap.com",
                "bulma.io",
                "materializecss.com",
            ]
        ):
            return "CSS Frameworks"

        if (
            any(k in full_text for k in ["color", "palette"])
            or "coolors.co" in url
            or "paletton.com" in url
            or "colorhunt.co" in url
        ):
            return "Colores"

        if (
            any(k in full_text for k in ["font", "tipografia"])
            or "fonts.google.com" in url
            or "fontsquirrel.com" in url
            or "dafont.com" in url
        ):
            return "Tipografia"

        # Diseño y UI
        if (
            any(k in full_text for k in ["inspiration", "design showcase"])
            or "dribbble.com" in url
            or "behance.net" in url
            or "awwwards.com" in url
        ):
            return "Inspiracion Diseno"

        if (
            any(k in full_text for k in ["wireframe", "prototype"])
            or "figma.com" in url
            or "sketch.com" in url
            or "adobe.com/xd" in url
        ):
            return "Herramientas Diseno"

        if (
            any(k in full_text for k in ["component", "ui kit"])
            or "uiverse.io" in url
            or "uiball.com" in url
            or "loading.io" in url
        ):
            return "Componentes UI"

        # HTML y estructura
        if "html" in full_text and "css" not in full_text:
            return "HTML"

        # JavaScript y frameworks
        if ("javascript" in full_text or "js" in full_text) and "json" not in full_text:
            if "vanilla" in full_text or "javascript.info" in url:
                return "JavaScript Vanilla"

        if "react" in full_text or "react.dev" in url or "reactjs.org" in url:
            return "React"
        if "vue" in full_text or "vuejs.org" in url:
            return "Vue"
        if "angular" in full_text or "angular.io" in url:
            return "Angular"
        if "svelte" in full_text or "svelte.dev" in url:
            return "Svelte"
        if "next" in full_text or "nextjs.org" in url:
            return "Next.js"
        if "typescript" in full_text or "typescriptlang.org" in url:
            return "TypeScript"

        # Backend
        if (
            "node" in full_text
            or "express" in full_text
            or "nodejs.org" in url
            or "expressjs.com" in url
        ):
            return "Node.js"

        if (
            "python" in full_text
            or "python.org" in url
            or "django" in full_text
            or "flask" in full_text
            or "fastapi" in full_text
        ):
            return "Python Backend"

        if "php" in full_text or "laravel" in full_text or "symfony" in full_text:
            return "PHP"

        if (
            "java" in full_text
            and "javascript" not in full_text
            or "spring" in full_text
        ):
            return "Java"

        if (
            any(k in full_text for k in ["api", "rest", "graphql"])
            or "postman.com" in url
            or "insomnia.rest" in url
        ):
            return "APIs"

        # Documentación oficial
        if (
            "/docs" in url
            or "/documentation" in url
            or "documentation" in title
        ) and "google.com/drive" not in url:
            return "Documentacion"

        if any(
            d in url for d in ["developer.mozilla.org", "w3schools.com", "devdocs.io"]
        ):
            return "Referencias Web"

        # Bases de datos
        if any(
            k in full_text
            for k in ["sql", "mysql", "postgres", "sqlite", "database"]
        ):
            return "SQL Databases"

        if any(
            k in full_text for k in ["mongodb", "nosql", "redis", "firebase"]
        ):
            return "NoSQL Databases"

        # DevOps y deployment
        if any(k in full_text for k in ["docker", "kubernetes", "container"]):
            return "Docker Kubernetes"

        if (
            "aws" in full_text
            or "amazon web services" in full_text
            or "aws.amazon.com" in url
        ):
            return "AWS"

        if "azure" in full_text or "azure.microsoft.com" in url:
            return "Azure"
        if "heroku" in full_text or "heroku.com" in url:
            return "Heroku"
        if "netlify" in full_text or "netlify.com" in url:
            return "Netlify"
        if "vercel" in full_text or "vercel.com" in url:
            return "Vercel"

        if any(k in full_text for k in ["deploy", "hosting", "cloud"]):
            return "Hosting Deploy"

        # Control de versiones
        if "git" in full_text and "github.com" not in url and "gitlab.com" not in url:
            return "Git"

        # Testing
        if any(k in full_text for k in ["test", "jest", "cypress", "selenium", "junit"]):
            return "Testing"

        # Herramientas de desarrollo
        if any(
            d in url
            for d in [
                "codepen.io",
                "codesandbox.io",
                "stackblitz.com",
                "replit.com",
                "jsfiddle.net",
            ]
        ):
            return "Editores Online"

        if "regex" in full_text or "regex101.com" in url or "regexr.com" in url:
            return "Regex"

        if (
            any(k in full_text for k in ["convert", "transform", "generator"])
            or "transform.tools" in url
            or ("json" in url and "format" in full_text)
        ):
            return "Convertidores"

        if any(k in full_text for k in ["minif", "compress", "optimize"]):
            return "Optimizacion"

        # Iconos e imágenes
        if (
            "icon" in full_text
            or "fontawesome.com" in url
            or "iconmonstr.com" in url
            or "feathericons.com" in url
            or "heroicons.com" in url
        ):
            return "Iconos"

        if (
            any(k in full_text for k in ["image", "photo", "stock"])
            or "unsplash.com" in url
            or "pexels.com" in url
            or "pixabay.com" in url
        ):
            return "Imagenes"

        # IA y ML
        if (
            any(
                k in full_text
                for k in [
                    "ai",
                    "artificial intelligence",
                    "chatgpt",
                    "openai",
                    "machine learning",
                    "deep learning",
                ]
            )
            or "huggingface.co" in url
            or "openai.com" in url
        ):
            return "Inteligencia Artificial"

        # Contenido multimedia
        if "youtube.com" in url or "youtu.be" in url:
            return "YouTube"
        if "vimeo.com" in url:
            return "Vimeo"

        # Blogs y artículos
        if "medium.com" in url:
            return "Medium"
        if "dev.to" in url:
            return "Dev.to"
        if "hashnode.com" in url:
            return "Hashnode"

        if any(k in full_text for k in ["blog", "article", "tutorial"]):
            return "Blogs Tutoriales"

        # Comunidad
        if "stackoverflow.com" in url or "stackexchange.com" in url:
            return "Stack Overflow"
        if "reddit.com" in url:
            return "Reddit"
        if "discord." in url:
            return "Discord"

        # Email y comunicación
        if (
            "resend.com" in url
            or "sendgrid.com" in url
            or "email service" in full_text
        ):
            return "Email Services"

        # Recursos y listas
        if any(
            k in full_text for k in ["awesome", "resource", "recurso", "collection", "list"]
        ):
            return "Recursos Colecciones"

        # Cheat sheets
        if any(k in full_text for k in ["cheat", "reference", "quick"]):
            return "Cheat Sheets"

        # Fallback: intenta categorizar por dominio conocido
        try:
            domain = url.split("/")[2] if len(url.split("/")) > 2 else ""
            if domain:
                if "microsoft.com" in domain:
                    return "Microsoft"
                if "google.com" in domain:
                    return "Google"
                if "amazon.com" in domain:
                    return "Amazon"
        except IndexError:
            pass

        return "Sin Categorizar"
