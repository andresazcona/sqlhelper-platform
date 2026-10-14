"""Generate sqlhelper-platform.drawio (3 pages). Python 3 stdlib only.

python docs/diagrams/gen_drawio.py
"""

from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).with_name("sqlhelper-platform.drawio")

COMPUTE, STORAGE, NETWORK = "#ED7100", "#7AA116", "#8C4FFF"
SECURITY, MANAGEMENT, INTEGRATION = "#DD344C", "#E7157B", "#E7157B"
BLUE, RED, GREY, GREEN = "#1A73E8", "#C62828", "#888888", "#2E7D32"

ICON = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={color};"
    "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
    "html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;"
    "resIcon=mxgraph.aws4.{res};"
)
GROUP = (
    "points=[];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
    "fontStyle=1;container=0;pointerEvents=0;collapsible=0;recursiveResize=0;"
    "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{icon};strokeColor={color};fillColor=none;"
    "verticalAlign=top;align=left;spacingLeft=30;fontColor={color};dashed={dashed};"
)
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;arcSize={arc};fillColor={fill};strokeColor={stroke};"
    "fontSize=12;align={align};verticalAlign={valign};spacing=10;"
)
EDGE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=2;"
    "strokeColor={color};fontColor={color};fontSize=11;labelBackgroundColor=#ffffff;"
    "dashed={dashed};{extra}"
)
DIAMOND = (
    "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;fontSize=12;fontStyle=1;"
)


def label(name: str, detail: str = "", cost: str = "") -> str:
    parts = [f"<b>{name}</b>"]
    if detail:
        parts.append(f'<span style="font-size:11px;color:#666;">{detail}</span>')
    if cost:
        parts.append(f'<span style="font-size:11px;color:{GREEN};">{cost}</span>')
    return "<br>".join(parts)


class Page:
    def __init__(self, name: str, title: str, subtitle: str):
        self.name, self.cells, self.n = name, [], 0
        self.text(
            40,
            20,
            1200,
            50,
            f'<b style="font-size:20px;">{title}</b><br>'
            f'<span style="font-size:12px;color:#666;">{subtitle}</span>',
        )

    def _id(self) -> str:
        self.n += 1
        return f"{self.name}-{self.n}"

    def vertex(self, value: str, style: str, x, y, w, h) -> str:
        cid = self._id()
        self.cells.append(
            f'<mxCell id="{cid}" value={quoteattr(value)} style={quoteattr(style)} vertex="1" '
            f'parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
            "</mxCell>"
        )
        return cid

    def text(self, x, y, w, h, value: str, align: str = "left") -> str:
        style = f"text;html=1;align={align};verticalAlign=top;whiteSpace=wrap;fontSize=12;"
        return self.vertex(value, style, x, y, w, h)

    def icon(self, x, y, res, color, value, size=78) -> str:
        return self.vertex(value, ICON.format(color=color, res=res), x, y, size, size)

    def group(self, x, y, w, h, value, icon, color, dashed=0, fill="none") -> str:
        style = GROUP.format(icon=icon, color=color, dashed=dashed)
        return self.vertex(value, style.replace("fillColor=none", f"fillColor={fill}"), x, y, w, h)

    def box(
        self,
        x,
        y,
        w,
        h,
        value,
        fill="#ffffff",
        stroke="#666666",
        align="center",
        valign="middle",
        arc=8,
    ) -> str:
        style = BOX.format(fill=fill, stroke=stroke, align=align, valign=valign, arc=arc)
        return self.vertex(value, style, x, y, w, h)

    def diamond(self, x, y, value, w=170, h=110) -> str:
        return self.vertex(value, DIAMOND, x, y, w, h)

    def edge(
        self,
        src,
        tgt,
        value="",
        color=BLUE,
        dashed=0,
        exit=None,
        entry=None,
        points=(),
        label_offset=None,
    ) -> None:
        extra = ""
        if exit:
            extra += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
        if entry:
            extra += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
        style = EDGE.format(color=color, dashed=dashed, extra=extra)
        pts = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points)
        geo = '<mxGeometry relative="1" as="geometry">'
        if pts:
            geo += f'<Array as="points">{pts}</Array>'
        if label_offset:
            geo += f'<mxPoint x="{label_offset[0]}" y="{label_offset[1]}" as="offset"/>'
        geo += "</mxGeometry>"
        self.cells.append(
            f'<mxCell id="{self._id()}" value={quoteattr(value)} style={quoteattr(style)} '
            f'edge="1" parent="1" source="{src}" target="{tgt}">{geo}</mxCell>'
        )

    def xml(self) -> str:
        return (
            f'<diagram id="{self.name}" name="{self.name}"><mxGraphModel dx="1900" dy="1200" '
            'grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            'page="1" pageScale="1" pageWidth="1900" pageHeight="1200" math="0" shadow="0">'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(self.cells)
            + "</root></mxGraphModel></diagram>"
        )


DEVTOOLS, DARK = "#C925D1", "#232F3E"
NOTE = dict(fill="#f5f5f5", stroke="#999999", align="left", valign="top")
MONO = "font-family:monospace;font-size:11px;"

# Cost model (us-east-1, 730 h/month, low traffic): see README.
COST = {
    "dev": ("$54", "Fargate 1 x 0.25 vCPU / 0.5 GB $7", "ALB $18", "3 interface endpoints x 1 AZ $22"),
    "staging": ("$62", "Fargate 2 x 0.25 vCPU / 0.5 GB $14", "ALB $18", "3 interface endpoints x 1 AZ $22"),
    "prod": ("$104", "Fargate 2 x 0.5 vCPU / 1 GB $29", "ALB $20", "3 interface endpoints x 2 AZ $44"),
}
COST_REST = {
    "dev": "CloudFront $1 · Route 53 $1 · CloudWatch $4 · ECR + S3 $0.5",
    "staging": "CloudFront $1 · Route 53 $1 · CloudWatch $5 · ECR + S3 $0.5",
    "prod": "CloudFront $3 · Route 53 $1 · CloudWatch $7 · ECR + S3 $0.5",
}
ENV_COLORS = {
    "dev": ("#FFF2CC", "#D6B656"),
    "staging": ("#DAE8FC", "#6C8EBF"),
    "prod": ("#D5E8D4", "#82B366"),
}


def cost_box(p, env, x, y, w, h):
    total, fargate, alb, endpoints = COST[env]
    fill, stroke = ENV_COLORS[env]
    extra = "<br>Autoscaling to 6 tasks adds ~$14 per task-month" if env == "prod" else ""
    p.box(
        x,
        y,
        w,
        h,
        f"<b>{env}: ~{total} / month</b> (not deployed)<br>"
        f'<span style="font-size:11px;">{fargate} · {alb} · {endpoints}<br>'
        f"{COST_REST[env]}{extra}</span>",
        fill=fill,
        stroke=stroke,
        align="left",
        valign="top",
    )


def infra() -> Page:
    p = Page(
        "1 - Production infrastructure",
        "SQLhelper on AWS: production",
        "CloudFront · S3 (OAC) · internal ALB · ECS Fargate arm64 · VPC endpoints, no NAT · "
        "CodeDeploy · CloudWatch · Terraform",
    )
    users = p.icon(50, 330, "users", DARK, label("Users", "browser"))
    p.group(180, 100, 1700, 910, "AWS account: prod (us-east-1)", "group_account", "#CD2264")
    r53 = p.icon(235, 130, "route_53", NETWORK, label("Route 53", "A / AAAA alias", "~ $1 / mo"))
    acm = p.icon(
        235,
        480,
        "certificate_manager",
        SECURITY,
        label("ACM certificate", "DNS-validated", "$0"),
    )
    cf = p.icon(420, 330, "cloudfront", NETWORK, label("CloudFront", "TLS 1.2+ · HTTP/3", "~ $3 / mo"))
    s3 = p.icon(
        640,
        200,
        "s3",
        STORAGE,
        label("S3 frontend", "private · versioned", "~ $0.1 / mo"),
    )

    vpc = p.group(
        800,
        130,
        1040,
        670,
        "VPC 10.30.0.0/16 · 2 AZs · private subnets only, no NAT gateway",
        "group_vpc",
        "#8C4FFF",
        fill="#E6F2F8",
    )
    alb = p.icon(
        870,
        330,
        "elastic_load_balancing",
        NETWORK,
        label("Internal ALB", "HTTP :80 · blue / green TGs", "~ $20 / mo"),
    )
    p.icon(
        870,
        560,
        "endpoints",
        NETWORK,
        label("S3 gateway endpoint", "ECR image layers", "$0"),
    )
    for az, y in (("a", 160), ("b", 450)):
        p.group(
            1060,
            y,
            770,
            260,
            f"Private subnet · us-east-1{az}",
            "group_subnet",
            "#DD344C",
            fill="#FBE8E8",
        )
    task_a = p.icon(
        1110,
        225,
        "fargate",
        COMPUTE,
        label("Fargate task", "api · 0.5 vCPU · 1 GB", "arm64 · ~ $14 / mo"),
    )
    ep_a = p.icon(
        1430,
        225,
        "endpoints",
        NETWORK,
        label("Interface endpoints", "ecr.api · ecr.dkr · logs", "~ $22 / mo per AZ"),
    )
    task_b = p.icon(
        1110,
        515,
        "fargate",
        COMPUTE,
        label("Fargate task", "api · 0.5 vCPU · 1 GB", "arm64 · ~ $14 / mo"),
    )
    p.icon(
        1430,
        515,
        "endpoints",
        NETWORK,
        label("Interface endpoints", "ecr.api · ecr.dkr · logs", "~ $22 / mo per AZ"),
    )

    p.edge(users, r53, "DNS", color=GREY, dashed=1, exit=(0.5, 0), entry=(0, 0.5))
    p.edge(users, cf, "HTTPS :443", exit=(1, 0.5), entry=(0, 0.35))
    p.edge(r53, cf, "alias", color=GREY, dashed=1, exit=(1, 0.5), entry=(0.3, 0))
    p.edge(acm, cf, "TLS cert", color=GREY, dashed=1, exit=(1, 0.5), entry=(0, 0.75), points=((380, 519), (380, 388)))
    p.edge(cf, s3, "/* default · OAC", exit=(0.7, 0), entry=(0, 0.5))
    p.edge(cf, alb, "/api/* · VPC origin", exit=(1, 0.5), entry=(0, 0.5))
    p.edge(alb, task_a, "HTTP :3000", exit=(1, 0.5), entry=(0, 0.5))
    p.edge(alb, task_b, "", exit=(1, 0.5), entry=(0, 0.5))
    p.edge(task_a, ep_a, "HTTPS :443", color=GREY, dashed=1, exit=(1, 0.5), entry=(0, 0.5))

    by = 850
    ecr = p.icon(
        860,
        by,
        "ecr",
        COMPUTE,
        label("Amazon ECR", "immutable tags · scan", "~ $0.1 / mo"),
    )
    cw = p.icon(
        1080,
        by,
        "cloudwatch_2",
        MANAGEMENT,
        label("CloudWatch", "logs · 5 alarms · dashboard", "~ $7 / mo"),
    )
    sns = p.icon(
        1300, by, "sns", MANAGEMENT, label("SNS topic", "alarm email", "$0")
    )
    cd = p.icon(
        1520,
        by,
        "codedeploy",
        DEVTOOLS,
        label("CodeDeploy", "blue/green · canary", "$0"),
    )
    p.edge(vpc, ecr, "image pull", color=GREY, dashed=1, exit=(0.0952, 1), entry=(0.5, 0))
    p.edge(vpc, cw, "logs + metrics", color=GREY, dashed=1, exit=(0.3067, 1), entry=(0.5, 0))
    p.edge(cw, sns, "alarm", color=RED, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(cd, vpc, "swaps ALB target groups", color=DEVTOOLS, dashed=1, exit=(0.5, 0), entry=(0.73, 1))

    p.box(
        200,
        650,
        590,
        250,
        "<b>Network and access</b><br>"
        "• ALB SG: :80 only from the CloudFront origin-facing prefix list<br>"
        "• Task SG: :3000 only from the ALB SG; egress :443 to the endpoints and the S3 prefix list<br>"
        "• Endpoint SG: :443 from the VPC CIDR · no public IPs · the internet gateway exists only "
        "because VPC origins need it, no route points at it<br><br>"
        "<b>IAM</b><br>"
        "• Execution role: pull from ECR, write logs. No task role: the API is stateless and calls "
        "no AWS service<br>"
        "• Deploys use a GitHub OIDC role scoped to one environment (page 2)<br><br>"
        "<b>Alarms (SNS email)</b><br>"
        "• API 5xx &gt; 5 / min for 3 min · p95 latency &gt; 1.5 s (both also roll back releases)<br>"
        "• No running tasks · CPU &gt; 85 % · CloudFront 5xx rate &gt; 5 %",
        **NOTE,
    )
    cost_box(p, "dev", 40, 1040, 900, 100)
    cost_box(p, "prod", 960, 1040, 900, 100)
    return p


def step(p, y, h, text, fill="#ffffff", stroke=DARK):
    return p.box(60, y, 460, h, text, fill=fill, stroke=stroke, align="left", valign="middle")


def panel(p, x, y, title, blue, green, caption, stroke="#666666"):
    p.box(x, y, 160, 210, "", fill="#ffffff", stroke=stroke)
    p.text(x + 10, y + 8, 140, 36, f"<b>{title}</b>", align="center")
    for i, (name, pct, color) in enumerate((("Blue (v1)", blue, BLUE), ("Green (v2)", green, GREEN))):
        by = y + 48 + i * 52
        shown = f"{name} · {pct} %" if 0 < pct < 30 else name
        p.text(x + 15, by, 130, 18, f'<span style="font-size:11px;">{shown}</span>')
        p.box(x + 15, by + 20, 130, 22, "", fill="#eeeeee", stroke="#cccccc", arc=0)
        if pct:
            p.box(
                x + 15,
                by + 20,
                round(130 * pct / 100),
                22,
                f'<span style="font-size:11px;color:#fff;"><b>{pct} %</b></span>' if pct >= 30 else "",
                fill=color,
                stroke=color,
                arc=0,
            )
    p.text(x + 10, y + 156, 140, 50, f'<span style="font-size:11px;">{caption}</span>', align="center")


def cicd() -> Page:
    p = Page(
        "2 - CI/CD and blue-green",
        "Delivery: GitHub Actions to CodeDeploy blue/green",
        "OIDC federation (no stored keys) · ECR · task definition revision · CodeDeploy · "
        "S3 sync · CloudFront invalidation",
    )
    p.box(40, 110, 500, 930, "", fill="#F6F8FA", stroke=DARK, arc=2)
    p.text(60, 118, 460, 24, "<b>GitHub: andresazcona/sqlhelper-platform</b>")
    step(
        p,
        150,
        90,
        "<b>ci.yml</b> · pull_request and push to main<br>"
        '<span style="font-size:11px;">terraform fmt -check · validate (4 roots) · tflint · checkov<br>'
        "needs no AWS credentials</span>",
        fill="#f5f5f5",
        stroke="#999999",
    )
    b2 = step(p, 260, 50, "<b>1</b>  deploy.yml · workflow_dispatch (environment, app_ref)")
    b3 = step(
        p,
        330,
        70,
        "<b>2</b>  preflight job, inside the GitHub Environment<br>"
        '<span style="font-size:11px;">no-op unless vars.AWS_ROLE_ARN is set</span>',
    )
    b4 = step(
        p,
        480,
        80,
        "<b>3</b>  api job (arm64 runner)<br>"
        '<span style="font-size:11px;">checkout app repo · docker build · docker push :sha-run</span>',
    )
    b5 = step(
        p,
        620,
        90,
        "<b>4</b>  release<br>"
        '<span style="font-size:11px;">render task definition with the new image · register revision · '
        "CodeDeploy create-deployment with appspec.yaml</span>",
    )
    b6 = step(
        p,
        740,
        80,
        "<b>5</b>  frontend job (needs api)<br>"
        '<span style="font-size:11px;">vite build · s3 sync (hashed assets immutable) · '
        "index.html no-cache</span>",
    )
    b7 = step(p, 910, 50, "<b>6</b>  cloudfront create-invalidation /index.html")
    for a, b in ((b2, b3), (b3, b4), (b4, b5), (b5, b6), (b6, b7)):
        p.edge(a, b, "", color=DARK, dashed=1, exit=(0.5, 1), entry=(0.5, 0))

    p.group(600, 110, 500, 930, "AWS account (one per environment)", "group_account", "#CD2264")
    iam = p.icon(
        650,
        321,
        "identity_and_access_management",
        SECURITY,
        label("GitHub OIDC role", "sub = repo:owner/repo:", "environment:prod · 1 h"),
    )
    ecr = p.icon(
        650, 481, "ecr", COMPUTE, label("Amazon ECR", "push to one repository")
    )
    cd = p.icon(
        900, 626, "codedeploy", DEVTOOLS, label("CodeDeploy", "1 app · 1 deployment group")
    )
    s3 = p.icon(650, 741, "s3", STORAGE, label("S3 frontend", "PutObject on one bucket"))
    cf = p.icon(900, 886, "cloudfront", NETWORK, label("CloudFront", "invalidate one distribution"))
    p.edge(b3, iam, "OIDC token", color=DARK, dashed=1, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(b4, ecr, "docker push", color=DARK, dashed=1, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(b5, cd, "create-deployment", color=DARK, dashed=1, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(b6, s3, "s3 sync / cp", color=DARK, dashed=1, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(b7, cf, "", color=DARK, dashed=1, exit=(1, 0.5), entry=(0, 0.5))

    p.group(1140, 110, 740, 930, "Blue / green on ECS Fargate", "group_region", "#00A4A6", dashed=1)
    alb = p.icon(1180, 170, "elastic_load_balancing", NETWORK, label("Internal ALB", "listener :80"))
    blue = p.box(
        1450,
        150,
        380,
        90,
        "<b>Target group blue</b> · task set v1 (live)<br>"
        '<span style="font-size:11px;">tasks run the previous image</span>',
        fill="#DAE8FC",
        stroke="#6C8EBF",
    )
    green = p.box(
        1450,
        270,
        380,
        90,
        "<b>Target group green</b> · task set v2 (new)<br>"
        '<span style="font-size:11px;">same task definition family, new image · /health checks</span>',
        fill="#D5E8D4",
        stroke="#82B366",
    )
    p.edge(alb, blue, "live", color=BLUE, exit=(1, 0.5), entry=(0, 0.5))
    p.edge(alb, green, "canary", color=GREEN, exit=(1, 0.5), entry=(0, 0.5))
    cw = p.icon(1180, 400, "cloudwatch_2", MANAGEMENT, label("CloudWatch alarms", "5xx · p95 latency"))
    p.edge(cd, alb, "shift traffic", color=DEVTOOLS, dashed=1, exit=(0.5, 0), entry=(0, 0.5))
    p.edge(
        cw,
        cd,
        "alarm: stop + roll back",
        color=RED,
        exit=(0, 0.5),
        entry=(1, 0.5),
        points=((1060, 439), (1060, 665)),
    )

    p.text(
        1160,
        520,
        690,
        24,
        "<b>Traffic during a prod release</b> (CodeDeployDefault.ECSCanary10Percent5Minutes)",
    )
    panel(p, 1160, 555, "T0 · steady state", 100, 0, "v1 serves everything", stroke=BLUE)
    panel(p, 1340, 555, "T1 · canary, 5 min", 90, 10, "alarms watched; healthy goes on", stroke=GREEN)
    panel(p, 1520, 555, "T2 · switched", 0, 100, "blue kept 5 min, then terminated", stroke=GREEN)
    panel(p, 1700, 555, "Alarm fires", 100, 0, "stop, route back to blue, stop green", stroke=RED)
    p.box(
        1160,
        790,
        700,
        140,
        "<b>Release rules</b><br>"
        "• dev uses ECSAllAtOnce (no canary); staging and prod use the canary above<br>"
        "• Rollback gates: &lt;env&gt;-api-5xx and &lt;env&gt;-api-latency-p95, plus deployment failure<br>"
        "• The ECS service uses the CODE_DEPLOY controller; Terraform ignores task definition, "
        "target group and desired count after the first apply<br>"
        "• Frontend goes live only after the API job succeeds; old hashed assets are never "
        "deleted, so open tabs keep working",
        **NOTE,
    )
    return p


def tree_text() -> str:
    lines = [
        ("sqlhelper-platform/", ""),
        ("|-- bootstrap/", "state bucket, local state"),
        ("|-- modules/", ""),
        ("|   |-- network/", "VPC, subnets, endpoints"),
        ("|   |-- ecr/", "repository, lifecycle"),
        ("|   |-- api/", "ALB, Fargate, CodeDeploy"),
        ("|   |-- edge/", "S3, CloudFront, ACM, DNS"),
        ("|   |-- monitoring/", "alarms, SNS, dashboard"),
        ("|   `-- github-oidc/", "OIDC provider + role"),
        ("|-- envs/", ""),
        ("|   |-- dev/", "own backend key"),
        ("|   |-- staging/", ""),
        ("|   `-- prod/", ""),
        ("|-- deploy/appspec.yaml", ""),
        ("`-- .github/workflows/", "ci.yml · deploy.yml"),
    ]
    out = []
    for name, note in lines:
        pad = "&nbsp;" * max(1, 34 - len(name))
        n = name.replace(" ", "&nbsp;")
        out.append(f"{n}{pad}<span style='color:#888;'>{note}</span>" if note else n)
    return f'<span style="{MONO}">' + "<br>".join(out) + "</span>"


ENV_TEXT = {
    "dev": (
        "VPC 10.10.0.0/16 · endpoints in 1 AZ<br>"
        "API: 1 task · 0.25 vCPU / 0.5 GB · no autoscaling<br>"
        "Releases: ECSAllAtOnce, no canary<br>"
        "Logs 14 days · ALB deletion protection off"
    ),
    "staging": (
        "VPC 10.20.0.0/16 · endpoints in 1 AZ<br>"
        "API: 2 to 3 tasks · 0.25 vCPU / 0.5 GB · CPU autoscaling<br>"
        "Releases: canary 10 % / 5 min (same as prod)<br>"
        "Logs 30 days · ALB deletion protection off"
    ),
    "prod": (
        "VPC 10.30.0.0/16 · endpoints in both AZs<br>"
        "API: 2 to 6 tasks · 0.5 vCPU / 1 GB · CPU autoscaling<br>"
        "Releases: canary 10 % / 5 min, alarm rollback<br>"
        "Logs 90 days · ALB deletion protection on"
    ),
}


def environments() -> Page:
    p = Page(
        "3 - Environments and state",
        "Environments and Terraform state layout",
        "one AWS account per environment · one S3 state bucket per account · "
        "native S3 locking (use_lockfile) · shared local modules",
    )
    p.box(40, 110, 520, 290, tree_text(), fill="#f5f5f5", stroke="#999999", align="left", valign="top")
    p.box(
        40,
        420,
        520,
        260,
        "<b>State layout</b><br>"
        "• bootstrap/ runs once per account with local state and creates "
        "<span style='font-family:monospace;'>sqlhelper-tfstate-&lt;account&gt;</span>: "
        "versioned, encrypted, public access blocked, TLS-only policy, old versions kept 90 days<br>"
        "• Each envs/* root then points its s3 backend at that bucket with its own key and "
        "<span style='font-family:monospace;'>use_lockfile = true</span>: Terraform 1.10+ locks "
        "with a conditional write of a .tflock object, so there is no DynamoDB table to create, "
        "pay for or keep in sync<br>"
        "• Blast radius: a bad apply in dev cannot touch prod state, resources or IAM; "
        "the account boundary is the isolation<br>"
        "• allowed_account_ids in every provider block stops an env being applied to the wrong account<br>"
        "• Account ids shown are placeholders",
        **NOTE,
    )
    mods = p.box(
        600,
        110,
        1260,
        70,
        "<b>modules/</b> · network · ecr · api · edge · monitoring · github-oidc<br>"
        '<span style="font-size:11px;">identical code in every environment; only the inputs '
        "(sizes, counts, CIDR, deploy config, retention) differ</span>",
        fill="#EDE7F6",
        stroke="#8C4FFF",
    )
    xs = {"dev": 600, "staging": 1030, "prod": 1460}
    accounts = {"dev": "111111111111", "staging": "222222222222", "prod": "333333333333"}
    for env, x0 in xs.items():
        acct = accounts[env]
        fill, stroke = ENV_COLORS[env]
        grp = p.group(x0, 230, 400, 430, f"Account {acct}: {env}", "group_account", "#CD2264")
        stack = p.box(
            x0 + 20,
            280,
            360,
            150,
            f"<b>envs/{env}</b><br>"
            f'<span style="font-size:11px;">{ENV_TEXT[env]}<br>'
            "Stack: network · ecr · api · edge · monitoring · github-oidc</span>",
            fill=fill,
            stroke=stroke,
            align="left",
            valign="top",
        )
        bucket = p.icon(
            x0 + 161,
            470,
            "s3",
            STORAGE,
            label("S3 state bucket", f"sqlhelper-tfstate-{acct}", f"key {env}/terraform.tfstate"),
        )
        p.edge(
            mods,
            stack,
            "",
            color="#8C4FFF",
            exit=((x0 + 20 + 0.92 * 360 - 600) / 1260, 1),
            entry=(0.92, 0),
        )
        p.edge(stack, bucket, "init · plan · apply", color=GREY, exit=(0.5, 1), entry=(0.5, 0))
        gh = p.box(
            x0,
            710,
            400,
            100,
            f"<b>GitHub environment: {env}</b><br>"
            '<span style="font-size:11px;">vars: AWS_ROLE_ARN · FRONTEND_BUCKET · '
            "CLOUDFRONT_DISTRIBUTION_ID<br>copied from the stack output "
            "github_environment_variables; protection rules (reviewers) live here</span>",
            fill="#F6F8FA",
            stroke=DARK,
            align="left",
            valign="top",
        )
        p.edge(gh, grp, "OIDC deploy role", color=DARK, dashed=1, exit=(0.5, 0), entry=(0.5, 1))
        cost_box(p, env, x0, 850, 400, 100)
    return p


def main() -> None:
    pages = [infra(), cicd(), environments()]
    OUT.write_text(
        '<mxfile host="gen_drawio.py">' + "".join(pg.xml() for pg in pages) + "</mxfile>\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()
